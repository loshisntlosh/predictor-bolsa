class QuantMatrixError(Exception):
    """Excepción base para la terminal cuantitativa."""
    pass

class MarketDataFetchError(QuantMatrixError):
    """Se lanza cuando el proveedor de datos falla o entrega datos corruptos."""
    pass