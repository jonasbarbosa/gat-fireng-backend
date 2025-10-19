# Torna 'api' um pacote e reexporta db/migrate para permitir imports como 'from .. import db' nos modelos
from .models import db, migrate

__all__ = ['db', 'migrate']