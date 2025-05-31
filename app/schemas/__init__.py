# Import các schema Pydantic
from .Employee import (
    TaiKhoanNhanVienBase,
    TaiKhoanNhanVienCreate,
    TaiKhoanNhanVienUpdate,
    TaiKhoanNhanVienInDB,
)

from .Booking_Ticket import (
    PhieuDatChoVeMayBayBase,
    PhieuDatChoVeMayBayCreate,
    PhieuDatChoVeMayBayUpdate,
    PhieuDatChoVeMayBayInDB,
)

from .TicketClassStatistics import ThongKeHangVeChuyenBayInDB
from .hangve import HangVeInDB
from .tuyenbay import TuyenBayInDB
from .sanbay import SanBayBase, SanBayInDB, SanBayCreate, SanBayUpdate
from .Flight import ChuyenBayBase, ChuyenBayCreate, ChuyenBayInDB, ChuyenBayUpdate
from .TicketPrice import DonGiaBase, DonGiaCreate, DonGiaInDB, DonGiaUpdate
from .FlightDetail import ChiTietChuyenBayBase, ChiTietChuyenBayCreate, ChiTietChuyenBayInDB, ChiTietChuyenBayUpdate
TuyenBayInDB.model_rebuild()
PhieuDatChoVeMayBayInDB.model_rebuild()
ThongKeHangVeChuyenBayInDB.model_rebuild()
HangVeInDB.model_rebuild()
TaiKhoanNhanVienInDB.model_rebuild()  
