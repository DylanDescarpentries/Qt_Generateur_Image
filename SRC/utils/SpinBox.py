from PySide6.QtWidgets import QSpinBox
from PySide6.QtCore import Qt, QTimer, QPoint


class SpinBox(QSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._resetSpeed)
        self._initialStep = 1
        self._currentStep = self._initialStep
        self._accelerationFactor = 2
        self._maximumStep = 50
        self.setMouseTracking(True)
        self._dragStartPos = QPoint()
        self._dragging = False

    def wheelEvent(self, event):
        """Réimplémentation de l'événement de molette pour accélérer le changement de valeur."""
        if not self._timer.isActive():
            # Si le timer n'est pas actif, c'est le début d'une nouvelle séquence d'événements de molette
            self._currentStep = self._initialStep
        else:
            # Si le timer est déjà actif, on accélère
            self._currentStep = min(
                self._currentStep * self._accelerationFactor, self._maximumStep
            )

        self._timer.start(100)  # Réinitialise le timer à chaque événement de molette

        # Calcul de la direction de la rotation de la molette et application du pas actuel
        numDegrees = event.angleDelta().y() / 8
        numSteps = numDegrees / 15  # Qt utilise par défaut 15 degrés par pas de molette
        self.stepBy(int(numSteps * self._currentStep))

        event.accept()  # Marque l'événement comme traité

    def _resetSpeed(self):
        """Réinitialise le pas à sa valeur initiale après un délai sans utilisation de la molette."""
        self._currentStep = self._initialStep

    """Gestion du cliqué glissé pour modifier la valeur du SpinBox"""

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragStartPos = event.pos()
            self._dragging = True
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._dragging:
            # Calculez la différence de mouvement depuis le début du "tirage"
            diff = event.pos() - self._dragStartPos
            # Ajustez la valeur en fonction de la différence verticale
            # Vous pouvez ajuster 'factor' pour rendre la spinbox plus ou moins sensible
            factor = 1
            self.setValue(self.value() + (diff.y() // factor))
            self._dragStartPos = event.pos()
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self._dragging:
            self._dragging = False
            event.accept()
