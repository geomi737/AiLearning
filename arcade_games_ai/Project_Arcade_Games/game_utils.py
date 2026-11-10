"""
Утилиты для совместимости игр с Linux / Python 3.14.
Обеспечивает безопасную загрузку изображений и звуков,
даже если SDL2_image или SDL2_mixer не установлены.
"""
import pygame
import os

# --- Безопасная загрузка изображений ---

def _load_image_pillow(path):
    """Загружает изображение через Pillow (фолбэк для отсутствующего SDL2_image)."""
    from PIL import Image
    pil_image = Image.open(path).convert("RGBA")
    return pygame.image.fromstring(pil_image.tobytes(), pil_image.size, "RGBA")


def load_image(path):
    """Загружает изображение, пробуя сначала pygame, потом Pillow."""
    try:
        return pygame.image.load(path)
    except pygame.error:
        return _load_image_pillow(path)


# --- Безопасная работа со звуком ---

_mixer_available = None  # кэш результата инициализации

def init_mixer():
    """Инициализирует pygame.mixer, если он доступен. Возвращает True/False."""
    global _mixer_available
    if _mixer_available is not None:
        return _mixer_available
    try:
        pygame.mixer.init()
        _mixer_available = True
    except Exception:
        _mixer_available = False
        print("Предупреждение: pygame.mixer недоступен, звук отключён.")
    return _mixer_available


def load_sound(path):
    """Безопасно загружает звуковой файл. Возвращает Sound или None."""
    if not init_mixer():
        return None
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None


def load_music(path):
    """Безопасно загружает и запускает фоновую музыку."""
    if not init_mixer():
        return
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
    except Exception:
        pass


def stop_music():
    """Безопасно останавливает музыку."""
    if _mixer_available:
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
        except Exception:
            pass


def resume_music():
    """Безопасно возобновляет музыку."""
    if _mixer_available:
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
        except Exception:
            pass


def play_sound(sound):
    """Безопасно воспроизводит звук."""
    if _mixer_available and sound:
        try:
            sound.play()
        except Exception:
            pass
