import os
import pickle
import requests
import numpy as np
from django.core.management.base import BaseCommand
from django.conf import settings
from main.models import CustomUser


def extract_embedding(image):
    import cv2
    import mediapipe as mp
    mp_face_mesh = mp.solutions.face_mesh
    with mp_face_mesh.FaceMesh(
            static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5
    ) as face_mesh:
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if not results.multi_face_landmarks:
            return None
        landmarks = results.multi_face_landmarks[0].landmark
        return np.array([(lm.x, lm.y, lm.z) for lm in landmarks]).flatten()


def download_image_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        import cv2
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return image
    except Exception as e:
        print(f"Couldn't load image from {url}: {e}")
        return None


class Command(BaseCommand):
    help = "Trains the face recognition model using profile picture URLs from the database."

    def handle(self, *args, **options):
        from sklearn.neighbors import KNeighborsClassifier

        self.stdout.write(
            self.style.SUCCESS("Starting face recognition model training using URLs...")
        )

        users = CustomUser.objects.exclude(profile_image_url__isnull=True).exclude(profile_image_url__exact='')

        if not users.exists():
            self.stdout.write(
                self.style.WARNING("No users with valid profile_image_url found. Nothing to train.")
            )
            return

        embeddings = []
        labels = []

        for user in users:
            self.stdout.write(f"Processing user: {user.username} (ID: {user.id}) from URL: {user.profile_image_url}")
            image = download_image_from_url(user.profile_image_url)

            if image is None:
                self.stdout.write(
                    self.style.ERROR(f"Failed to download or decode image for user {user.username}")
                )
                continue

            embedding = extract_embedding(image)

            if embedding is not None:
                embeddings.append(embedding)
                labels.append(user.id)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"----> Successfully processed face for user: {user.username}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"----> Could not detect face for user: {user.username}"
                    )
                )

        if not embeddings:
            self.stdout.write(
                self.style.ERROR(
                    "No faces were detected in any of the provided images. Model was not trained or saved.")
            )
            return

        k = min(len(labels), 3)
        if k == 0:
            self.stdout.write(self.style.ERROR("No samples to train on. Aborting."))
            return

        if len(set(labels)) < k:
            k = len(set(labels))

        self.stdout.write(f"Training KNN model with {k} neighbor(s)...")
        knn_clf = KNeighborsClassifier(n_neighbors=k, algorithm="ball_tree", weights="distance")
        knn_clf.fit(embeddings, labels)

        model_dir = os.path.join(settings.BASE_DIR, "face_models")
        os.makedirs(model_dir, exist_ok=True)

        model_path = os.path.join(model_dir, "face_classifier.pkl")
        with open(model_path, "wb") as f:
            pickle.dump(knn_clf, f)
        self.stdout.write(self.style.SUCCESS(f"Classifier model saved to {model_path}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Training complete! {len(labels)} faces processed. Models saved in {model_dir}"
            )
        )
