try:
    from app import app
except ImportError:
    # Fallback para execução como pacote
    from .app import app