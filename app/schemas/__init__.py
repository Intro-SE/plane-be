# Import các schema Pydantic
from .taikhoannhanvien import (
    TaiKhoanNhanVienBase,
    TaiKhoanNhanVienCreate,
    TaiKhoanNhanVienUpdate,
    TaiKhoanNhanVienInDB,
)

from .phieudatcho_vemaybay import (
    PhieuDatChoVeMayBayBase,
    PhieuDatChoVeMayBayCreate,
    PhieuDatChoVeMayBayUpdate,
    PhieuDatChoVeMayBayInDB,
)

from .thongkehangvechuyenbay import ThongKeHangVeChuyenBayInDB
from .hangve import HangVeInDB
from .tuyenbay import TuyenBayInDB
from .sanbay import SanBayBase, SanBayInDB, SanBayCreate, SanBayUpdate
from .chuyenbay import ChuyenBayBase, ChuyenBayCreate, ChuyenBayInDB, ChuyenBayUpdate
from .dongia import DonGiaBase, DonGiaCreate, DonGiaInDB, DonGiaUpdate
from .chitietchuyenbay import ChiTietChuyenBayBase, ChiTietChuyenBayCreate, ChiTietChuyenBayInDB, ChiTietChuyenBayUpdate
TuyenBayInDB.model_rebuild()
PhieuDatChoVeMayBayInDB.model_rebuild()
ThongKeHangVeChuyenBayInDB.model_rebuild()
HangVeInDB.model_rebuild()
TaiKhoanNhanVienInDB.model_rebuild()  
