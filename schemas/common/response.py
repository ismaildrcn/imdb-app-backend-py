from typing import Generic, TypeVar, Optional, Any, List
from pydantic import BaseModel, Field

# Generic veri tipi için TypeVar
T = TypeVar('T')


class ErrorDetail(BaseModel):
    """Hata detayları için model"""
    field: Optional[str] = Field(None, description="Hata ile ilişkili alan")
    message: str = Field(..., description="Hata mesajı")
    code: Optional[str] = Field(None, description="Hata kodu")


class PaginationMeta(BaseModel):
    """Sayfalama bilgileri için model"""
    page: int = Field(..., description="Mevcut sayfa")
    page_size: int = Field(..., description="Sayfa başına öğe sayısı")
    total_items: int = Field(..., description="Toplam öğe sayısı")
    total_pages: int = Field(..., description="Toplam sayfa sayısı")


class BaseResponse(BaseModel, Generic[T]):
    """
    Standart API yanıt modeli
    
    Örnek Kullanım:
    
    # Başarılı yanıt (veri ile)
    return BaseResponse(
        success=True,
        message="İşlem başarılı",
        data=user_data
    )
    
    # Başarılı yanıt (veri olmadan)
    return BaseResponse(
        success=True,
        message="Kullanıcı silindi"
    )
    
    # Hata yanıtı
    return BaseResponse(
        success=False,
        message="İşlem başarısız",
        errors=[
            ErrorDetail(field="email", message="Geçersiz email formatı", code="INVALID_EMAIL")
        ]
    )
    
    # Sayfalama ile
    return BaseResponse(
        success=True,
        data=movies,
        meta=PaginationMeta(page=1, page_size=20, total_items=100, total_pages=5)
    )
    """
    success: bool = Field(..., description="İşlem başarılı mı?")
    message: Optional[str] = Field(None, description="Kullanıcıya gösterilecek mesaj")
    data: Optional[T] = Field(None, description="Yanıt verisi")
    errors: Optional[List[ErrorDetail]] = Field(None, description="Hata detayları")
    meta: Optional[Any] = Field(None, description="Meta veriler (pagination, vb.)")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "İşlem başarıyla tamamlandı",
                "data": {
                    "id": 1,
                    "name": "Örnek Veri"
                },
                "errors": None,
                "meta": None
            }
        }


# Kolaylık fonksiyonları
def success_response(
    data: Any = None,
    message: str = "İşlem başarılı",
    meta: Any = None
) -> BaseResponse:
    """Başarılı yanıt oluşturur"""
    return BaseResponse(
        success=True,
        message=message,
        data=data,
        meta=meta
    )


def error_response(
    message: str = "İşlem başarısız",
    errors: List[ErrorDetail] = None,
    data: Any = None
) -> BaseResponse:
    """Hata yanıtı oluşturur"""
    return BaseResponse(
        success=False,
        message=message,
        errors=errors or [],
        data=data
    )


def paginated_response(
    data: List[Any],
    page: int,
    page_size: int,
    total_items: int,
    message: str = "İşlem başarılı"
) -> BaseResponse:
    """Sayfalama ile yanıt oluşturur"""
    total_pages = (total_items + page_size - 1) // page_size
    
    return BaseResponse(
        success=True,
        message=message,
        data=data,
        meta=PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages
        )
    )
