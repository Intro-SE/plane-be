-- B1: Tạo bảng + PK
CREATE TABLE Rules
(
    max_airports INT DEFAULT 10 CHECK (max_airports >= 0),
	max_transit_airports INT DEFAULT 2 CHECK (max_transit_airports >= 0),
    min_flight_time INT DEFAULT 30 CHECK (min_flight_time > 0),
	min_stop_time INT DEFAULT 10 CHECK (min_stop_time > 0),
	max_stop_time INT DEFAULT 20 CHECK (max_stop_time >= min_stop_time),
    latest_booking_time INT DEFAULT 1 CHECK (latest_booking_time > 0),
	latest_cancel_time INT DEFAULT 1 CHECK (latest_cancel_time > 0),
	ticket_class_count INT DEFAULT 2 CHECK (ticket_class_count > 0)
);

CREATE TABLE Airport
(
	airport_id VARCHAR(50) NOT NULL,
	airport_name VARCHAR(50) NOT NULL,
	airport_address VARCHAR(50) NOT NULL,
	CONSTRAINT PK_Airport PRIMARY KEY (airport_id)
);


CREATE TABLE FlightRoute
(
	flight_route_id VARCHAR(50) NOT NULL,
	departure_airport_id VARCHAR(50) NOT NULL,
	arrival_airport_id VARCHAR(50) NOT NULL,
	CONSTRAINT PK_FlightRoute PRIMARY KEY (flight_route_id)
);

CREATE TABLE Flight
(
	flight_id VARCHAR(50) NOT NULL,
	flight_route_id VARCHAR(50) NOT NULL,
	flight_date DATE NOT NULL,
	departure_time TIME NOT NULL,
	flight_duration INT NOT NULL,
	flight_seat_count INT NOT NULL,
	CONSTRAINT PK_Flight PRIMARY KEY (flight_id)
);

CREATE TABLE FlightDetail
(
	flight_detail_id VARCHAR(50) NOT NULL,
	flight_route_id VARCHAR(50) NOT NULL,
	transit_airport_id VARCHAR(50) NOT NULL,
	stop_time INT NOT NULL,
	note VARCHAR(200),
	CONSTRAINT PK_FlightDetail PRIMARY KEY (flight_detail_id)
);

CREATE TABLE TicketClass
(
	ticket_class_id VARCHAR(50) NOT NULL,
	ticket_class_name VARCHAR(50) NOT NULL,
	CONSTRAINT PK_TicketClass PRIMARY KEY (ticket_class_id)
);

CREATE TABLE TicketClassStatistics
(
	ticket_class_statistics_id varchar(50) NOT NULL,
	flight_id VARCHAR(50) NOT NULL,
	ticket_class_id VARCHAR(50) NOT NULL,
	total_seats INT NOT NULL,	-- Số lượng ghế của hạng vé trong chuyến bay đó --
	available_seats INT NOT NULL,	-- Số lượng ghế trống của hạng vé đó --
	booked_seats INT NOT NULL,		-- Số lượng ghế đã đặt, lấy từ các vé của chuyến bay --
	CONSTRAINT PK_TicketClassStatistics PRIMARY KEY (ticket_class_statistics_id)
);

CREATE TABLE TicketPrice
(
	ticket_price_id VARCHAR(50) NOT NULL,
	flight_route_id VARCHAR(50) NOT NULL,
	ticket_class_id VARCHAR(50) NOT NULL,
	price INT NOT NULL,
	CONSTRAINT PK_TicketPrice PRIMARY KEY (ticket_price_id)
);

CREATE TABLE Employee
(
	employee_id VARCHAR(50) NOT NULL,
	employee_username VARCHAR(200) NOT NULL,
	employee_password VARCHAR(200) NOT NULL,
	employee_name VARCHAR(50) NOT NULL,
	national_id VARCHAR(50) NOT NULL,
	gender VARCHAR(3) CHECK (Gender IN ('Nam', 'Nữ')),
	phone_number VARCHAR(50) NOT NULL,
	created_date DATE NOT NULL,
	CONSTRAINT PK_Employee PRIMARY KEY (employee_id)
);

CREATE TABLE Booking_Ticket
(
	booking_ticket_id VARCHAR(50) NOT NULL,
	flight_id VARCHAR(50) NOT NULL,
	-- Thông tin Hành khách
	passenger_name VARCHAR(50) NOT NULL,
	national_id VARCHAR(50) NOT NULL,
	gender VARCHAR(3) CHECK (Gender IN ('Nam', 'Nữ')),
	phone_number VARCHAR(12) NOT NULL,
	-- Thông tin vé
	ticket_class_id VARCHAR(50) NOT NULL,
	booking_price BIGINT NOT NULL,
	booking_date DATE NOT NULL,
	-- -- Quan trọng: True (Đã xuất vé - Là vé chuyến bay), False (Chỉ là phiếu đặt chỗ)
	ticket_status BOOLEAN NOT NULL,
	-- Thông tin nhân viên
	employee_id VARCHAR(50) NOT NULL,
	CONSTRAINT PK_Booking_Ticket PRIMARY KEY (booking_ticket_id)
); -- Tới đây

------------------------------------------------

-- THÊM FK + Ràng buộc
-- Bảng Flight
ALTER TABLE Flight
    ADD CONSTRAINT FK_Flight_FlightRoute
    FOREIGN KEY (flight_route_id)
    REFERENCES FlightRoute(flight_route_id);

-- Bảng Airport

-- Bảng FlightRoute
ALTER TABLE FlightRoute
    ADD CONSTRAINT FK_FlightRoute_DepartureAirport
    FOREIGN KEY (departure_airport_id)
    REFERENCES Airport(airport_id);

ALTER TABLE FlightRoute
    ADD CONSTRAINT FK_FlightRoute_ArrivalAirport
    FOREIGN KEY (arrival_airport_id)
    REFERENCES Airport(airport_id);

-- alter table PHIM
-- 	add constraint CK_PHIM_NAMSX
-- 	check (NAMSX <= year(getdate()))

-- Bảng FlightDetail
ALTER TABLE FlightDetail
    ADD CONSTRAINT FK_FlightDetail_FlightRoute
    FOREIGN KEY (flight_route_id)
    REFERENCES FlightRoute(flight_route_id);

ALTER TABLE FlightDetail
    ADD CONSTRAINT FK_FlightDetail_TransitAirport
    FOREIGN KEY (transit_airport_id)
    REFERENCES Airport(airport_id);

-- ALTER TABLE PHIM
--     ADD CONSTRAINT CK_PHIM_NAMSX
--     CHECK (NAMSX <= EXTRACT(YEAR FROM CURRENT_DATE));

-- Bảng HANGVE

-- Bảng TicketClassStatistics 
ALTER TABLE TicketClassStatistics
    ADD CONSTRAINT FK_TicketClassStatistics_Flight
    FOREIGN KEY (flight_id)
    REFERENCES Flight(flight_id);

ALTER TABLE TicketClassStatistics
    ADD CONSTRAINT FK_TicketClassStatistics_TicketClass
    FOREIGN KEY (ticket_class_id)
    REFERENCES TicketClass(ticket_class_id);

-- Bảng DONGIA
ALTER TABLE TicketPrice
    ADD CONSTRAINT FK_TicketPrice_FlightRoute
    FOREIGN KEY (flight_route_id)
    REFERENCES FlightRoute(flight_route_id);

ALTER TABLE TicketPrice
    ADD CONSTRAINT FK_TicketPrice_TicketClass
    FOREIGN KEY (ticket_class_id)
    REFERENCES TicketClass(ticket_class_id);

-- ALTER TABLE DAODIEN
--     ADD CONSTRAINT FK_DAODIEN_PHAI
--     CHECK (PHAI IN ('Nam', 'Nữ'));

-- alter table DAODIEN
-- 	add constraint FK_DAODIEN_NAMSINH
-- 	check (year(getdate()) - NAMSINH >= 18)

-- Bảng Employee

-- Bảng Booking_Ticket
ALTER TABLE Booking_Ticket
    ADD CONSTRAINT FK_Booking_Ticket_Flight
    FOREIGN KEY (flight_id)
    REFERENCES Flight(flight_id);

ALTER TABLE Booking_Ticket
    ADD CONSTRAINT FK_Booking_Ticket_TicketClass
    FOREIGN KEY (ticket_class_id)
    REFERENCES TicketClass(ticket_class_id);

ALTER TABLE Booking_Ticket
    ADD CONSTRAINT FK_Booking_Ticket_Employee
    FOREIGN KEY (employee_id)
    REFERENCES Employee(employee_id);

-- ALTER TABLE DIENVIEN
--     ADD CONSTRAINT FK_DIENVIEN_PHAI
--     CHECK (PHAI IN ('Nam', 'Nữ'));

--------------------------------------------
-- Nhập DL
-- Rules
INSERT INTO Rules VALUES (10, 2, 30, 10, 20, 1, 1, 2);

-- Airport
INSERT INTO Airport VALUES 
('SB01', 'Nội Bài', 'Hà Nội'),
('SB02', 'Tân Sơn Nhất', 'TP. HCM'),
('SB03', 'Đà Nẵng', 'Đà Nẵng'),
('SB04', 'Cần Thơ', 'Cần Thơ'),
('SB05', 'Cam Ranh', 'Khánh Hòa'),
('SB06', 'Phú Bài', 'Huế'),
('SB07', 'Liên Khương', 'Lâm Đồng'),
('SB08', 'Vinh', 'Nghệ An'),
('SB09', 'Chu Lai', 'Quảng Nam'),
('SB10', 'Pleiku', 'Gia Lai');

-- FlightRoute (20 tuyến bay từ các sân bay khác nhau)
INSERT INTO FlightRoute VALUES 
('TB01', 'SB01', 'SB02'), ('TB02', 'SB02', 'SB03'), ('TB03', 'SB03', 'SB04'),
('TB04', 'SB04', 'SB05'), ('TB05', 'SB05', 'SB06'), ('TB06', 'SB06', 'SB07'),
('TB07', 'SB07', 'SB08'), ('TB08', 'SB08', 'SB09'), ('TB09', 'SB09', 'SB10'),
('TB10', 'SB10', 'SB01'), ('TB11', 'SB01', 'SB03'), ('TB12', 'SB02', 'SB04'),
('TB13', 'SB03', 'SB05'), ('TB14', 'SB04', 'SB06'), ('TB15', 'SB05', 'SB07'),
('TB16', 'SB06', 'SB08'), ('TB17', 'SB07', 'SB09'), ('TB18', 'SB08', 'SB10'),
('TB19', 'SB09', 'SB01'), ('TB20', 'SB10', 'SB02');

-- Flight
INSERT INTO Flight VALUES 
('CB01', 'TB01', '2025-06-01', '08:00:00', 90, 180),
('CB02', 'TB02', '2025-06-02', '09:00:00', 60, 180),
('CB03', 'TB03', '2025-06-03', '10:00:00', 75, 180),
('CB04', 'TB04', '2025-06-04', '11:00:00', 90, 180),
('CB05', 'TB05', '2025-06-05', '12:00:00', 100, 180),
('CB06', 'TB06', '2025-06-06', '13:00:00', 85, 180),
('CB07', 'TB07', '2025-06-07', '14:00:00', 120, 180),
('CB08', 'TB08', '2025-06-08', '15:00:00', 130, 180),
('CB09', 'TB09', '2025-06-09', '16:00:00', 95, 180),
('CB10', 'TB10', '2025-06-10', '17:00:00', 110, 180);

-- FlightDetail
INSERT INTO FlightDetail VALUES 
('CTCB01', 'TB01', 'SB03', 15, 'Dừng nạp nhiên liệu'),
('CTCB02', 'TB02', 'SB04', 20, 'Dừng kỹ thuật'),
('CTCB03', 'TB03', 'SB05', 10, 'Dừng ăn trưa'),
('CTCB04', 'TB04', 'SB06', 15, ''),
('CTCB05', 'TB05', 'SB07', 10, ''),
('CTCB06', 'TB06', 'SB08', 20, ''),
('CTCB07', 'TB07', 'SB09', 15, ''),
('CTCB08', 'TB08', 'SB10', 10, ''),
('CTCB09', 'TB09', 'SB01', 10, ''),
('CTCB10', 'TB10', 'SB02', 20, '');

-- TicketClass
INSERT INTO TicketClass VALUES 
('HV01', 'Phổ thông'),
('HV02', 'Thương gia'),
('HV03', 'Hạng nhất');

-- TicketClassStatistics
INSERT INTO TicketClassStatistics VALUES 
('TK01', 'CB01', 'HV01', 100, 70, 30),
('TK02', 'CB01', 'HV02', 50, 45, 5),
('TK03', 'CB01', 'HV03', 30, 25, 5),
('TK04', 'CB02', 'HV01', 90, 85, 5),
('TK05', 'CB02', 'HV02', 60, 50, 10),
('TK06', 'CB03', 'HV01', 100, 90, 10),
('TK07', 'CB03', 'HV02', 50, 48, 2),
('TK08', 'CB04', 'HV01', 100, 100, 0),
('TK09', 'CB04', 'HV03', 30, 30, 0),
('TK10', 'CB05', 'HV01', 110, 100, 10),
('TK11', 'CB06', 'HV02', 60, 58, 2),
('TK12', 'CB07', 'HV01', 100, 80, 20),
('TK13', 'CB08', 'HV01', 90, 85, 5),
('TK14', 'CB09', 'HV02', 70, 70, 0),
('TK15', 'CB10', 'HV03', 20, 15, 5);

-- TicketPrice
INSERT INTO TicketPrice VALUES 
('DG01', 'TB01', 'HV01', 1000000), ('DG02', 'TB01', 'HV02', 2000000), ('DG03', 'TB01', 'HV03', 3000000),
('DG04', 'TB02', 'HV01', 950000),  ('DG05', 'TB02', 'HV02', 1950000), ('DG06', 'TB02', 'HV03', 2950000),
('DG07', 'TB03', 'HV01', 1100000), ('DG08', 'TB03', 'HV02', 2100000), ('DG09', 'TB03', 'HV03', 3100000),
('DG10', 'TB04', 'HV01', 1050000), ('DG11', 'TB05', 'HV01', 1200000), ('DG12', 'TB06', 'HV01', 1150000),
('DG13', 'TB07', 'HV01', 1250000), ('DG14', 'TB08', 'HV01', 1350000), ('DG15', 'TB09', 'HV01', 1400000);

-- Employee
INSERT INTO Employee VALUES 
('NV01', 'admin1', 'pass1', 'Nguyễn Văn A', '123456789', 'Nam', '0909000001', '2025-01-01'),
('NV02', 'admin2', 'pass2', 'Trần Thị B', '123456788', 'Nữ', '0909000002', '2025-01-02'),
('NV03', 'admin3', 'pass3', 'Lê Văn C', '123456787', 'Nam', '0909000003', '2025-01-03'),
('NV04', 'admin4', 'pass4', 'Phạm Thị D', '123456786', 'Nữ', '0909000004', '2025-01-04'),
('NV05', 'admin5', 'pass5', 'Hoàng Văn E', '123456785', 'Nam', '0909000005', '2025-01-05');

-- Booking_Ticket
INSERT INTO Booking_Ticket VALUES 
('PDC01', 'CB01', 'Lê Thị A', '111111111', 'Nữ', '0912340001', 'HV01', 1000000, '2025-05-01', TRUE, 'NV01'),
('PDC02', 'CB01', 'Nguyễn Văn B', '222222222', 'Nam', '0912340002', 'HV02', 2000000, '2025-05-01', FALSE, 'NV01'),
('PDC03', 'CB01', 'Trần Thị C', '333333333', 'Nữ', '0912340003', 'HV03', 3000000, '2025-05-01', TRUE, 'NV02'),
('PDC04', 'CB02', 'Phạm Văn D', '444444444', 'Nam', '0912340004', 'HV01', 950000, '2025-05-02', FALSE, 'NV02'),
('PDC05', 'CB02', 'Hoàng Thị E', '555555555', 'Nữ', '0912340005', 'HV02', 1950000, '2025-05-02', TRUE, 'NV03'),
('PDC06', 'CB03', 'Đặng Văn F', '666666666', 'Nam', '0912340006', 'HV01', 1100000, '2025-05-03', TRUE, 'NV03'),
('PDC07', 'CB03', 'Nguyễn Thị G', '777777777', 'Nữ', '0912340007', 'HV02', 2100000, '2025-05-03', FALSE, 'NV03'),
('PDC08', 'CB04', 'Lê Văn H', '888888888', 'Nam', '0912340008', 'HV01', 1050000, '2025-05-04', TRUE, 'NV04'),
('PDC09', 'CB05', 'Trần Thị I', '999999999', 'Nữ', '0912340009', 'HV01', 1200000, '2025-05-05', TRUE, 'NV05'),
('PDC10', 'CB06', 'Phạm Văn J', '101010101', 'Nam', '0912340010', 'HV02', 2100000, '2025-05-06', TRUE, 'NV01'),
('PDC11', 'CB07', 'Nguyễn Thị K', '121212121', 'Nữ', '0912340011', 'HV01', 1250000, '2025-05-07', FALSE, 'NV01'),
('PDC12', 'CB08', 'Đặng Văn L', '131313131', 'Nam', '0912340012', 'HV01', 1350000, '2025-05-08', TRUE, 'NV02'),
('PDC13', 'CB09', 'Hoàng Thị M', '141414141', 'Nữ', '0912340013', 'HV02', 2000000, '2025-05-09', TRUE, 'NV03'),
('PDC14', 'CB10', 'Nguyễn Văn N', '151515151', 'Nam', '0912340014', 'HV03', 3000000, '2025-05-10', FALSE, 'NV04'),
('PDC15', 'CB01', 'Trần Thị O', '161616161', 'Nữ', '0912340015', 'HV01', 1000000, '2025-05-11', TRUE, 'NV05'),
('PDC16', 'CB02', 'Lê Văn P', '171717171', 'Nam', '0912340016', 'HV01', 950000, '2025-05-12', FALSE, 'NV01'),
('PDC17', 'CB03', 'Phạm Thị Q', '181818181', 'Nữ', '0912340017', 'HV01', 1100000, '2025-05-13', TRUE, 'NV02'),
('PDC18', 'CB04', 'Nguyễn Văn R', '191919191', 'Nam', '0912340018', 'HV03', 3100000, '2025-05-14', TRUE, 'NV03'),
('PDC19', 'CB05', 'Trần Thị S', '202020202', 'Nữ', '0912340019', 'HV01', 1200000, '2025-05-15', TRUE, 'NV04'),
('PDC20', 'CB06', 'Lê Văn T', '212121212', 'Nam', '0912340020', 'HV02', 2100000, '2025-05-16', FALSE, 'NV05');



