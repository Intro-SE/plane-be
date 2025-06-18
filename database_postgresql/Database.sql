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
	booked_seats INT NOT NULL,		-- Số lượng ghế đã đặt, lấy từ các phiếu đặt chỗ của chuyến bay --
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

-- Bảng FlightDetail
ALTER TABLE FlightDetail
    ADD CONSTRAINT FK_FlightDetail_FlightRoute
    FOREIGN KEY (flight_route_id)
    REFERENCES FlightRoute(flight_route_id);

ALTER TABLE FlightDetail
    ADD CONSTRAINT FK_FlightDetail_TransitAirport
    FOREIGN KEY (transit_airport_id)
    REFERENCES Airport(airport_id);

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
-- 35 chuyến bay từ 20/6 - 30/6/2025
('CB001', 'TB01', '2025-06-20', '08:00:00', 90, 180),
('CB002', 'TB02', '2025-06-21', '09:00:00', 95, 180),
('CB003', 'TB03', '2025-06-22', '10:00:00', 100, 180),
('CB004', 'TB04', '2025-06-23', '11:00:00', 105, 180),
('CB005', 'TB05', '2025-06-24', '12:00:00', 110, 180),
('CB006', 'TB06', '2025-06-25', '13:00:00', 115, 180),
('CB007', 'TB07', '2025-06-26', '14:00:00', 120, 180),
('CB008', 'TB08', '2025-06-27', '15:00:00', 90, 180),
('CB009', 'TB09', '2025-06-28', '16:00:00', 95, 180),
('CB010', 'TB10', '2025-06-29', '17:00:00', 100, 180),
('CB011', 'TB11', '2025-06-20', '08:30:00', 110, 180),
('CB012', 'TB12', '2025-06-21', '09:30:00', 105, 180),
('CB013', 'TB13', '2025-06-22', '10:30:00', 115, 180),
('CB014', 'TB14', '2025-06-23', '11:30:00', 100, 180),
('CB015', 'TB15', '2025-06-24', '12:30:00', 95, 180),
('CB016', 'TB16', '2025-06-25', '13:30:00', 90, 180),
('CB017', 'TB17', '2025-06-26', '14:30:00', 85, 180),
('CB018', 'TB18', '2025-06-27', '15:30:00', 110, 180),
('CB019', 'TB19', '2025-06-28', '16:30:00', 105, 180),
('CB020', 'TB20', '2025-06-29', '17:30:00', 95, 180),
('CB021', 'TB01', '2025-06-20', '07:00:00', 100, 180),
('CB022', 'TB02', '2025-06-21', '07:15:00', 100, 180),
('CB023', 'TB03', '2025-06-22', '07:30:00', 100, 180),
('CB024', 'TB04', '2025-06-23', '07:45:00', 100, 180),
('CB025', 'TB05', '2025-06-24', '08:00:00', 100, 180),
('CB026', 'TB06', '2025-06-25', '08:15:00', 100, 180),
('CB027', 'TB07', '2025-06-26', '08:30:00', 100, 180),
('CB028', 'TB08', '2025-06-27', '08:45:00', 100, 180),
('CB029', 'TB09', '2025-06-28', '09:00:00', 100, 180),
('CB030', 'TB10', '2025-06-29', '09:15:00', 100, 180),
('CB031', 'TB11', '2025-06-30', '09:30:00', 100, 180),
('CB032', 'TB12', '2025-06-30', '10:00:00', 100, 180),
('CB033', 'TB13', '2025-06-30', '10:30:00', 100, 180),
('CB034', 'TB14', '2025-06-30', '11:00:00', 100, 180),
('CB035', 'TB15', '2025-06-30', '11:30:00', 100, 180),
-- 20 chuyến bay từ 1/6 - 19/6/2025
('CB036', 'TB16', '2025-06-01', '06:00:00', 90, 180),
('CB037', 'TB17', '2025-06-02', '07:00:00', 95, 180),
('CB038', 'TB18', '2025-06-03', '08:00:00', 100, 180),
('CB039', 'TB19', '2025-06-04', '09:00:00', 105, 180),
('CB040', 'TB20', '2025-06-05', '10:00:00', 110, 180),
('CB041', 'TB01', '2025-06-06', '11:00:00', 115, 180),
('CB042', 'TB02', '2025-06-07', '12:00:00', 120, 180),
('CB043', 'TB03', '2025-06-08', '13:00:00', 90, 180),
('CB044', 'TB04', '2025-06-09', '14:00:00', 95, 180),
('CB045', 'TB05', '2025-06-10', '15:00:00', 100, 180),
('CB046', 'TB06', '2025-06-11', '16:00:00', 105, 180),
('CB047', 'TB07', '2025-06-12', '17:00:00', 110, 180),
('CB048', 'TB08', '2025-06-13', '18:00:00', 115, 180),
('CB049', 'TB09', '2025-06-14', '19:00:00', 120, 180),
('CB050', 'TB10', '2025-06-15', '20:00:00', 90, 180),
('CB051', 'TB11', '2025-06-16', '21:00:00', 95, 180),
('CB052', 'TB12', '2025-06-17', '22:00:00', 100, 180),
('CB053', 'TB13', '2025-06-18', '23:00:00', 105, 180),
('CB054', 'TB14', '2025-06-19', '07:00:00', 110, 180),
('CB055', 'TB15', '2025-06-19', '08:00:00', 115, 180),
-- Tháng 1 – 5/2025 (25 chuyến)
('CB056', 'TB16', '2025-01-10', '08:00:00', 100, 180),
('CB057', 'TB17', '2025-01-15', '10:00:00', 100, 180),
('CB058', 'TB18', '2025-01-20', '12:00:00', 100, 180),
('CB059', 'TB19', '2025-01-25', '14:00:00', 100, 180),
('CB060', 'TB20', '2025-01-30', '16:00:00', 100, 180),
('CB061', 'TB01', '2025-02-10', '08:00:00', 100, 180),
('CB062', 'TB02', '2025-02-15', '10:00:00', 100, 180),
('CB063', 'TB03', '2025-02-20', '12:00:00', 100, 180),
('CB064', 'TB04', '2025-02-25', '14:00:00', 100, 180),
('CB065', 'TB05', '2025-02-28', '16:00:00', 100, 180),
('CB066', 'TB06', '2025-03-05', '08:00:00', 100, 180),
('CB067', 'TB07', '2025-03-10', '10:00:00', 100, 180),
('CB068', 'TB08', '2025-03-15', '12:00:00', 100, 180),
('CB069', 'TB09', '2025-03-20', '14:00:00', 100, 180),
('CB070', 'TB10', '2025-03-25', '16:00:00', 100, 180),
('CB071', 'TB11', '2025-04-05', '08:00:00', 100, 180),
('CB072', 'TB12', '2025-04-10', '10:00:00', 100, 180),
('CB073', 'TB13', '2025-04-15', '12:00:00', 100, 180),
('CB074', 'TB14', '2025-04-20', '14:00:00', 100, 180),
('CB075', 'TB15', '2025-04-25', '16:00:00', 100, 180),
('CB076', 'TB16', '2025-05-01', '08:00:00', 100, 180),
('CB077', 'TB17', '2025-05-05', '10:00:00', 100, 180),
('CB078', 'TB18', '2025-05-10', '12:00:00', 100, 180),
('CB079', 'TB19', '2025-05-15', '14:00:00', 100, 180),
('CB080', 'TB20', '2025-05-20', '16:00:00', 100, 180),
-- 20 chuyến bay năm 2024
('CB081', 'TB01', '2024-01-10', '08:00:00', 100, 180),
('CB082', 'TB02', '2024-02-15', '10:00:00', 100, 180),
('CB083', 'TB03', '2024-03-20', '12:00:00', 100, 180),
('CB084', 'TB04', '2024-04-25', '14:00:00', 100, 180),
('CB085', 'TB05', '2024-05-30', '16:00:00', 100, 180),
('CB086', 'TB06', '2024-06-05', '08:00:00', 100, 180),
('CB087', 'TB07', '2024-07-10', '10:00:00', 100, 180),
('CB088', 'TB08', '2024-08-15', '12:00:00', 100, 180),
('CB089', 'TB09', '2024-09-20', '14:00:00', 100, 180),
('CB090', 'TB10', '2024-10-25', '16:00:00', 100, 180),
('CB091', 'TB11', '2024-11-10', '08:00:00', 100, 180),
('CB092', 'TB12', '2024-12-15', '10:00:00', 100, 180),
('CB093', 'TB13', '2024-01-20', '12:00:00', 100, 180),
('CB094', 'TB14', '2024-02-25', '14:00:00', 100, 180),
('CB095', 'TB15', '2024-03-30', '16:00:00', 100, 180),
('CB096', 'TB16', '2024-04-05', '08:00:00', 100, 180),
('CB097', 'TB17', '2024-05-10', '10:00:00', 100, 180),
('CB098', 'TB18', '2024-06-15', '12:00:00', 100, 180),
('CB099', 'TB19', '2024-07-20', '14:00:00', 100, 180),
('CB100', 'TB20', '2024-08-25', '16:00:00', 100, 180),
-- 20 chuyến bay năm 2023
('CB101', 'TB01', '2023-01-05', '08:00:00', 100, 180),
('CB102', 'TB02', '2023-02-10', '10:00:00', 100, 180),
('CB103', 'TB03', '2023-03-15', '12:00:00', 100, 180),
('CB104', 'TB04', '2023-04-20', '14:00:00', 100, 180),
('CB105', 'TB05', '2023-05-25', '16:00:00', 100, 180),
('CB106', 'TB06', '2023-06-30', '08:00:00', 100, 180),
('CB107', 'TB07', '2023-07-05', '10:00:00', 100, 180),
('CB108', 'TB08', '2023-08-10', '12:00:00', 100, 180),
('CB109', 'TB09', '2023-09-15', '14:00:00', 100, 180),
('CB110', 'TB10', '2023-10-20', '16:00:00', 100, 180),
('CB111', 'TB11', '2023-11-25', '08:00:00', 100, 180),
('CB112', 'TB12', '2023-12-30', '10:00:00', 100, 180),
('CB113', 'TB13', '2023-03-01', '08:00:00', 100, 180),
('CB114', 'TB14', '2023-05-01', '10:00:00', 100, 180),
('CB115', 'TB15', '2023-07-01', '12:00:00', 100, 180),
('CB116', 'TB16', '2023-09-01', '14:00:00', 100, 180),
('CB117', 'TB17', '2023-11-01', '16:00:00', 100, 180),
('CB118', 'TB18', '2023-01-15', '08:00:00', 100, 180),
('CB119', 'TB19', '2023-04-15', '10:00:00', 100, 180),
('CB120', 'TB20', '2023-08-15', '12:00:00', 100, 180);



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
('CTCB10', 'TB10', 'SB02', 20, ''),
('CTCB11', 'TB11', 'SB08', 10, 'Dừng kỹ thuật'),
('CTCB12', 'TB11', 'SB06', 15, 'Dừng ăn trưa'),
('CTCB13', 'TB12', 'SB09', 20, ''),
('CTCB14', 'TB12', 'SB10', 10, 'Dừng nạp nhiên liệu'),
('CTCB15', 'TB13', 'SB01', 15, ''),
('CTCB16', 'TB13', 'SB02', 15, 'Dừng kỹ thuật'),
('CTCB17', 'TB14', 'SB07', 10, ''),
('CTCB18', 'TB14', 'SB08', 15, 'Dừng ăn tối'),
('CTCB19', 'TB15', 'SB09', 10, ''),
('CTCB20', 'TB15', 'SB03', 20, 'Dừng kỹ thuật');



-- TicketClass
INSERT INTO TicketClass VALUES 
('HV01', 'Phổ thông'),
('HV02', 'Thương gia'),
('HV03', 'Hạng nhất'),
('HV04', 'Cao cấp');



-- TicketClassStatistics
INSERT INTO TicketClassStatistics VALUES 
-------- 35 chuyến bay từ 20/6 - 30/6/2025
-- CB001 (TB01 - HV01, HV02)
('TK001', 'CB001', 'HV01', 90, 87, 3), 
('TK002', 'CB001', 'HV02', 90, 89, 1),
-- CB002 (TB02 - HV02, HV03)
('TK003', 'CB002', 'HV02', 90, 88, 2), 
('TK004', 'CB002', 'HV03', 90, 89, 1),
-- CB003 (TB03 - HV01)
('TK005', 'CB003', 'HV01', 180, 178, 2),
-- CB004 (TB04 - HV01, HV02)
('TK006', 'CB004', 'HV01', 90, 90, 0), 
('TK007', 'CB004', 'HV02', 90, 88, 2),
-- CB005 (TB05 - HV03)
('TK008', 'CB005', 'HV03', 180, 179, 1),
-- CB006 (TB06 - HV01, HV04)
('TK009', 'CB006', 'HV01', 90, 88, 2), 
('TK010', 'CB006', 'HV04', 90, 87, 3),
-- CB007 (TB07 - HV02)
('TK011', 'CB007', 'HV02', 180, 178, 2),
-- CB008 (TB08 - HV02, HV03)
('TK012', 'CB008', 'HV02', 90, 87, 3), 
('TK013', 'CB008', 'HV03', 90, 90, 0),
-- CB009 (TB09 - HV01, HV02)
('TK014', 'CB009', 'HV01', 90, 87, 3), 
('TK015', 'CB009', 'HV02', 90, 89, 1),
-- CB010 (TB10 - HV01, HV03)
('TK016', 'CB010', 'HV01', 90, 88, 2), 
('TK017', 'CB010', 'HV03', 90, 89, 1),
-- CB011 (TB11 - HV01)
('TK018', 'CB011', 'HV01', 180, 177, 3), 
-- CB012 (TB12 - HV01, HV02)
('TK019', 'CB012', 'HV01', 90, 88, 2), 
('TK020', 'CB012', 'HV02', 90, 89, 1),
-- CB013 (TB13 - HV02, HV03)
('TK021', 'CB013', 'HV02', 90, 87, 3), 
('TK022', 'CB013', 'HV03', 90, 89, 1),
-- CB014 (TB14 - HV03)
('TK023', 'CB014', 'HV03', 180, 179, 1),
-- CB015 (TB15 - HV01)
('TK024', 'CB015', 'HV01', 180, 177, 3),
-- CB016 (TB16 - HV02, HV04)
('TK025', 'CB016', 'HV02', 90, 90, 0), 
('TK026', 'CB016', 'HV04', 90, 88, 2),
-- CB017 (TB17 - HV01)
('TK027', 'CB017', 'HV01', 180, 179, 1),
-- CB018 (TB18 - HV02, HV03)
('TK028', 'CB018', 'HV02', 90, 89, 1), 
('TK029', 'CB018', 'HV03', 90, 87, 3),
-- CB019 (TB19 - HV02)
('TK030', 'CB019', 'HV02', 180, 178, 2),
-- CB020 (TB20 - HV01, HV03) - Bỏ HV01
('TK031', 'CB020', 'HV03', 180, 177, 3),
-- CB021 (TB01 - HV01, HV02) – đủ 2 hạng
('TK032', 'CB021', 'HV01', 90, 87, 3),
('TK033', 'CB021', 'HV02', 90, 90, 0),
-- CB022 (TB02 - HV02, HV03) – đủ 2 hạng
('TK034', 'CB022', 'HV02', 90, 89, 1),
('TK035', 'CB022', 'HV03', 90, 88, 2),
-- CB023 (TB03 - HV01) – chỉ 1 hạng
('TK036', 'CB023', 'HV01', 180, 178, 2),
-- CB024 (TB04 - HV01, HV02) – đủ 2 hạng
('TK037', 'CB024', 'HV01', 90, 90, 0),
('TK038', 'CB024', 'HV02', 90, 89, 1),
-- CB025 (TB05 - HV03) – chỉ 1 hạng
('TK039', 'CB025', 'HV03', 180, 177, 3),
-- CB026 (TB06 - HV01, HV04) – đủ 2 hạng
('TK040', 'CB026', 'HV01', 90, 87, 3),
('TK041', 'CB026', 'HV04', 90, 90, 0),
-- CB027 (TB07 - HV02) – chỉ 1 hạng
('TK042', 'CB027', 'HV02', 180, 178, 2),
-- CB028 (TB08 - HV02, HV03) – đủ 2 hạng
('TK043', 'CB028', 'HV02', 90, 88, 2),
('TK044', 'CB028', 'HV03', 90, 89, 1),
-- CB029 (TB09 - HV01, HV02) – đủ 2 hạng
('TK045', 'CB029', 'HV01', 90, 90, 0),
('TK046', 'CB029', 'HV02', 90, 88, 2),
-- CB030 (TB10 - HV01, HV03) – đủ 2 hạng
('TK047', 'CB030', 'HV01', 90, 87, 3),
('TK048', 'CB030', 'HV03', 90, 90, 0),
-- CB031 (TB11 - HV01) – chỉ 1 hạng
('TK049', 'CB031', 'HV01', 180, 178, 2),
-- CB032 (TB12 - HV01, HV02) – skip HV02
('TK050', 'CB032', 'HV01', 180, 179, 1),
-- CB033 (TB13 - HV02, HV03) – skip HV03
('TK051', 'CB033', 'HV02', 180, 177, 3),
-- CB034 (TB14 - HV03) – chỉ 1 hạng
('TK052', 'CB034', 'HV03', 180, 179, 1),
-- CB035 (TB15 - HV01) – chỉ 1 hạng
('TK053', 'CB035', 'HV01', 180, 178, 2),


-------- 20 chuyến bay từ 1/6 - 19/6/2025 
-- CB036 (TB16 - HV02, HV04) – đủ 2 hạng
('TK054', 'CB036', 'HV02', 100, 98, 2),
('TK055', 'CB036', 'HV04', 80, 78, 2),
-- CB037 (TB17 - HV01) – chỉ 1 hạng
('TK056', 'CB037', 'HV01', 180, 177, 3),
-- CB038 (TB18 - HV02, HV03) – đủ 2 hạng
('TK057', 'CB038', 'HV02', 100, 98, 2),
('TK058', 'CB038', 'HV03', 80, 78, 2),
-- CB039 (TB19 - HV02) – chỉ 1 hạng
('TK059', 'CB039', 'HV02', 180, 177, 3),
-- CB040 (TB20 - HV01, HV03) – đủ 2 hạng
('TK060', 'CB040', 'HV01', 110, 108, 2),
('TK061', 'CB040', 'HV03', 70, 69, 1),
-- CB041 (TB01 - HV01, HV02) – đủ 2 hạng
('TK062', 'CB041', 'HV01', 90, 88, 2),
('TK063', 'CB041', 'HV02', 90, 89, 1),
-- CB042 (TB02 - HV02, HV03) – bỏ HV03
('TK064', 'CB042', 'HV02', 180, 177, 3),
-- CB043 (TB03 - HV01) – chỉ 1 hạng
('TK065', 'CB043', 'HV01', 180, 179, 1),
-- CB044 (TB04 - HV01, HV02) – đủ 2 hạng
('TK066', 'CB044', 'HV01', 100, 98, 2),
('TK067', 'CB044', 'HV02', 80, 78, 2),
-- CB045 (TB05 - HV03) – chỉ 1 hạng
('TK068', 'CB045', 'HV03', 180, 178, 2),
-- CB046 (TB06 - HV01, HV04) – đủ 2 hạng
('TK069', 'CB046', 'HV01', 90, 88, 2),
('TK070', 'CB046', 'HV04', 90, 89, 1),
-- CB047 (TB07 - HV02) – chỉ 1 hạng
('TK071', 'CB047', 'HV02', 180, 178, 2),
-- CB048 (TB08 - HV02, HV03) – đủ 2 hạng
('TK072', 'CB048', 'HV02', 115, 113, 2),
('TK073', 'CB048', 'HV03', 65, 63, 2),
-- CB049 (TB09 - HV01, HV02) – đủ 2 hạng
('TK074', 'CB049', 'HV01', 120, 117, 3),
('TK075', 'CB049', 'HV02', 60, 59, 1),
-- CB050 (TB10 - HV01, HV03) – đủ 2 hạng
('TK076', 'CB050', 'HV01', 100, 97, 3),
('TK077', 'CB050', 'HV03', 80, 78, 2),
-- CB051 (TB11 - HV01) – chỉ 1 hạng
('TK078', 'CB051', 'HV01', 180, 177, 3),
-- CB052 (TB12 - HV01, HV02) – đủ 2 hạng
('TK079', 'CB052', 'HV01', 100, 97, 3),
('TK080', 'CB052', 'HV02', 80, 78, 2),
-- CB053 (TB13 - HV02, HV03) – đủ 2 hạng
('TK081', 'CB053', 'HV02', 105, 104, 1),
('TK082', 'CB053', 'HV03', 75, 74, 1),
-- CB054 (TB14 - HV03) – chỉ 1 hạng
('TK083', 'CB054', 'HV03', 180, 179, 1),
-- CB055 (TB15 - HV01) – chỉ 1 hạng
('TK084', 'CB055', 'HV01', 180, 178, 2),


--------- Tháng 1 – 5/2025 (25 chuyến)
-- CB056 (TB16 - HV02, HV04) – đủ 2 hạng
('TK085', 'CB056', 'HV02', 90, 88, 2),
('TK086', 'CB056', 'HV04', 90, 89, 1),
-- CB057 (TB17 - HV01) – chỉ 1 hạng
('TK087', 'CB057', 'HV01', 180, 177, 3),
-- CB058 (TB18 - HV02, HV03) – đủ 2 hạng
('TK088', 'CB058', 'HV02', 100, 97, 3),
('TK089', 'CB058', 'HV03', 80, 80, 0),
-- CB059 (TB19 - HV02) – chỉ 1 hạng
('TK090', 'CB059', 'HV02', 180, 179, 1),
-- CB060 (TB20 - HV01, HV03) – đủ 2 hạng
('TK091', 'CB060', 'HV01', 100, 100, 0),
('TK092', 'CB060', 'HV03', 80, 78, 2),
-- CB061 (TB01 - HV01, HV02) – đủ 2 hạng
('TK093', 'CB061', 'HV01', 90, 88, 2),
('TK094', 'CB061', 'HV02', 90, 90, 0),
-- CB062 (TB02 - HV03, HV02) – đủ 2 hạng
('TK095', 'CB062', 'HV03', 100, 99, 1),
('TK096', 'CB062', 'HV02', 80, 80, 0),
-- CB063 (TB03 - HV01) – chỉ 1 hạng
('TK097', 'CB063', 'HV01', 180, 178, 2),
-- CB064 (TB04 - HV01, HV02) – đủ 2 hạng
('TK098', 'CB064', 'HV01', 100, 100, 0),
('TK099', 'CB064', 'HV02', 80, 78, 2),
-- CB065 (TB05 - HV03) – chỉ 1 hạng
('TK100', 'CB065', 'HV03', 180, 179, 1),
-- CB066 (TB06 - HV01, HV04) – đủ 2 hạng
('TK101', 'CB066', 'HV01', 90, 88, 2),
('TK102', 'CB066', 'HV04', 90, 88, 2),
-- CB067 (TB07 - HV02) – chỉ 1 hạng
('TK103', 'CB067', 'HV02', 180, 177, 3),
-- CB068 (TB08 - HV02, HV03) – đủ 2 hạng
('TK104', 'CB068', 'HV02', 100, 98, 2),
('TK105', 'CB068', 'HV03', 80, 78, 2),
-- CB069 (TB09 - HV01, HV02) – đủ 2 hạng
('TK106', 'CB069', 'HV01', 100, 98, 2),
('TK107', 'CB069', 'HV02', 80, 78, 2),
-- CB070 (TB10 - HV03, HV01) – đủ 2 hạng
('TK108', 'CB070', 'HV03', 100, 98, 2),
('TK109', 'CB070', 'HV01', 80, 79, 1),
-- CB071 (TB11 - HV01) – chỉ 1 hạng
('TK110', 'CB071', 'HV01', 180, 178, 2),
-- CB072 (TB12 - HV01, HV02) – đủ 2 hạng
('TK111', 'CB072', 'HV01', 100, 100, 0),
('TK112', 'CB072', 'HV02', 80, 78, 2),
-- CB073 (TB13 - HV02, HV03) – đủ 2 hạng
('TK113', 'CB073', 'HV02', 90, 89, 1),
('TK114', 'CB073', 'HV03', 90, 90, 0),
-- CB074 (TB14 - HV03) – chỉ 1 hạng
('TK115', 'CB074', 'HV03', 180, 180, 0),
-- CB075 (TB15 - HV01) – chỉ 1 hạng
('TK116', 'CB075', 'HV01', 180, 178, 2),
-- CB076 (TB16 - HV02, HV04) – đủ 2 hạng
('TK117', 'CB076', 'HV02', 100, 99, 1),
('TK118', 'CB076', 'HV04', 80, 80, 0),
-- CB077 (TB17 - HV01) – chỉ 1 hạng
('TK119', 'CB077', 'HV01', 180, 180, 0),
-- CB078 (TB18 - HV03, HV02) – đủ 2 hạng
('TK120', 'CB078', 'HV03', 100, 98, 2),
('TK121', 'CB078', 'HV02', 80, 78, 2),
-- CB079 (TB19 - HV02) – chỉ 1 hạng
('TK122', 'CB079', 'HV02', 180, 178, 2),
-- CB080 (TB20 - HV03, HV01) – đủ 2 hạng
('TK123', 'CB080', 'HV03', 100, 98, 2),
('TK124', 'CB080', 'HV01', 80, 78, 2),


-------- 20 chuyến bay năm 2024
-- CB081 (TB01 - HV01, HV02)
('TK125', 'CB081', 'HV01', 90, 88, 2), 
('TK126', 'CB081', 'HV02', 90, 89, 1),
-- CB082 (TB02 - HV02, HV03)
('TK127', 'CB082', 'HV02', 180, 178, 2),
-- CB083 (TB03 - HV01)
('TK128', 'CB083', 'HV01', 180, 179, 1),
-- CB084 (TB04 - HV01, HV02)
('TK129', 'CB084', 'HV01', 100, 97, 3), 
('TK130', 'CB084', 'HV02', 80, 78, 2),
-- CB085 (TB05 - HV03)
('TK131', 'CB085', 'HV03', 180, 178, 2),
-- CB086 (TB06 - HV01, HV04) - Bỏ HV01
('TK132', 'CB086', 'HV04', 180, 178, 2),
-- CB087 (TB07 - HV02)
('TK133', 'CB087', 'HV02', 180, 179, 1),
-- CB088 (TB08 - HV02, HV03)
('TK134', 'CB088', 'HV02', 100, 100, 0), 
('TK135', 'CB088', 'HV03', 80, 78, 2),
-- CB089 (TB09 - HV01, HV02) - Bỏ HV01
('TK136', 'CB089', 'HV02', 180, 177, 3),
-- CB090 (TB10 - HV01, HV03)
('TK137', 'CB090', 'HV01', 100, 98, 2), 
('TK138', 'CB090', 'HV03', 80, 80, 0),
-- CB091 (TB11 - HV01)
('TK139', 'CB091', 'HV01', 180, 178, 2),
-- CB092 (TB12 - HV01, HV02)
('TK140', 'CB092', 'HV01', 120, 119, 1), 
('TK141', 'CB092', 'HV02', 60, 60, 0),
-- CB093 (TB13 - HV02, HV03) - Bỏ HV02
('TK142', 'CB093', 'HV03', 180, 178, 2),
-- CB094 (TB14 - HV03)
('TK143', 'CB094', 'HV03', 180, 177, 3),
-- CB095 (TB15 - HV01)
('TK144', 'CB095', 'HV01', 180, 178, 2),
-- CB096 (TB16 - HV02, HV04)
('TK145', 'CB096', 'HV02', 90, 90, 0),
('TK146', 'CB096', 'HV04', 90, 88, 2),
-- CB097 (TB17 - HV01)
('TK147', 'CB097', 'HV01', 180, 178, 2),
-- CB098 (TB18 - HV02, HV03)
('TK148', 'CB098', 'HV02', 100, 97, 3), 
('TK149', 'CB098', 'HV03', 80, 80, 0),
-- CB099 (TB19 - HV02)
('TK150', 'CB099', 'HV02', 180, 178, 2),
-- CB100 (TB20 - HV01, HV03) – Bỏ HV03
('TK151', 'CB100', 'HV01', 180, 179, 1),

-------- 20 chuyến bay năm 2023
-- CB101 (TB01 - HV01, HV02)
('TK152', 'CB101', 'HV01', 90, 88, 2),
('TK153', 'CB101', 'HV02', 90, 87, 3),
-- CB102 (TB02 - HV02, HV03) – Bỏ HV03
('TK154', 'CB102', 'HV02', 180, 179, 1),
-- CB103 (TB03 - HV01)
('TK155', 'CB103', 'HV01', 180, 177, 3),
-- CB104 (TB04 - HV01, HV02) – đủ
('TK156', 'CB104', 'HV01', 100, 98, 2),
('TK157', 'CB104', 'HV02', 80, 78, 2),
-- CB105 (TB05 - HV03)
('TK158', 'CB105', 'HV03', 180, 180, 0),
-- CB106 (TB06 - HV01, HV04) – thiếu 1 hạng
('TK159', 'CB106', 'HV01', 180, 178, 2),
-- CB107 (TB07 - HV02)
('TK160', 'CB107', 'HV02', 180, 179, 1),
-- CB108 (TB08 - HV02, HV03) – đủ
('TK161', 'CB108', 'HV02', 100, 98, 2),
('TK162', 'CB108', 'HV03', 80, 77, 3),
-- CB109 (TB09 - HV01, HV02) – đủ
('TK163', 'CB109', 'HV01', 90, 90, 0),
('TK164', 'CB109', 'HV02', 90, 88, 2),
-- CB110 (TB10 - HV01, HV03) – Bỏ HV01
('TK165', 'CB110', 'HV03', 180, 178, 2),
-- CB111 (TB11 - HV01)
('TK166', 'CB111', 'HV01', 180, 177, 3),
-- CB112 (TB12 - HV01, HV02) – đủ
('TK167', 'CB112', 'HV01', 120, 118, 2),
('TK168', 'CB112', 'HV02', 60, 57, 3),
-- CB113 (TB13 - HV02, HV03) – đủ
('TK169', 'CB113', 'HV02', 90, 87, 3),
('TK170', 'CB113', 'HV03', 90, 89, 1),
-- CB114 (TB14 - HV03)
('TK171', 'CB114', 'HV03', 180, 178, 2),
-- CB115 (TB15 - HV01)
('TK172', 'CB115', 'HV01', 180, 180, 0),
-- CB116 (TB16 - HV02, HV04) – đủ
('TK173', 'CB116', 'HV02', 100, 97, 3),
('TK174', 'CB116', 'HV04', 80, 78, 2),
-- CB117 (TB17 - HV01)
('TK175', 'CB117', 'HV01', 180, 177, 3),
-- CB118 (TB18 - HV02, HV03) – đủ
('TK176', 'CB118', 'HV02', 100, 98, 2),
('TK177', 'CB118', 'HV03', 80, 79, 1),
-- CB119 (TB19 - HV02)
('TK178', 'CB119', 'HV02', 180, 180, 0),
-- CB120 (TB20 - HV01, HV03) – Bỏ HV03
('TK179', 'CB120', 'HV01', 180, 178, 2);



-- TicketPrice (30 dòng: 10 tuyến bay có 1 hạng vé, 20 tuyến có 2 hạng vé)
INSERT INTO TicketPrice VALUES
-- TB01 (2 hạng)
('DG01', 'TB01', 'HV01', 1000000), 
('DG02', 'TB01', 'HV02', 1500000),
-- TB02 (2 hạng)
('DG03', 'TB02', 'HV02', 1300000), 
('DG04', 'TB02', 'HV03', 1800000),
-- TB03 (1 hạng)
('DG05', 'TB03', 'HV01', 1100000),
-- TB04 (2 hạng)
('DG06', 'TB04', 'HV01', 1200000), 
('DG07', 'TB04', 'HV02', 1700000),
-- TB05 (1 hạng)
('DG08', 'TB05', 'HV03', 1900000),
-- TB06 (2 hạng)
('DG09', 'TB06', 'HV01', 1150000), 
('DG10', 'TB06', 'HV04', 2500000),
-- TB07 (1 hạng)
('DG11', 'TB07', 'HV02', 1350000),
-- TB08 (2 hạng)
('DG12', 'TB08', 'HV02', 1400000), 
('DG13', 'TB08', 'HV03', 1950000),
-- TB09 (2 hạng)
('DG14', 'TB09', 'HV01', 1000000), 
('DG15', 'TB09', 'HV02', 1450000),
-- TB10 (2 hạng)
('DG16', 'TB10', 'HV01', 1050000), 
('DG17', 'TB10', 'HV03', 1750000),
-- TB11 (1 hạng)
('DG18', 'TB11', 'HV01', 950000),
-- TB12 (2 hạng)
('DG19', 'TB12', 'HV01', 1100000), 
('DG20', 'TB12', 'HV02', 1600000),
-- TB13 (2 hạng)
('DG21', 'TB13', 'HV02', 1400000), 
('DG22', 'TB13', 'HV03', 2000000),
-- TB14 (1 hạng)
('DG23', 'TB14', 'HV03', 2100000),
-- TB15 (1 hạng)
('DG24', 'TB15', 'HV01', 1200000),
-- TB16 (2 hạng)
('DG25', 'TB16', 'HV02', 1500000), 
('DG26', 'TB16', 'HV04', 2400000),
-- TB17 (1 hạng)
('DG27', 'TB17', 'HV01', 1000000),
-- TB18 (2 hạng)
('DG28', 'TB18', 'HV02', 1350000), 
('DG29', 'TB18', 'HV03', 1850000),
-- TB19 (1 hạng)
('DG30', 'TB19', 'HV02', 1300000),
-- TB20 (2 hạng)
('DG31', 'TB20', 'HV01', 1350000), 
('DG32', 'TB20', 'HV03', 1850000);


-- Employee
INSERT INTO Employee VALUES 
('NV01', 'admin1', 'pass1', 'Nguyễn Văn A', '123456789', 'Nam', '0909000001', '2025-01-01'),
('NV02', 'admin2', 'pass2', 'Trần Thị B', '123456788', 'Nữ', '0909000002', '2025-01-02'),
('NV03', 'admin3', 'pass3', 'Lê Văn C', '123456787', 'Nam', '0909000003', '2025-01-03'),
('NV04', 'admin4', 'pass4', 'Phạm Thị D', '123456786', 'Nữ', '0909000004', '2025-01-04'),
('NV05', 'admin5', 'pass5', 'Hoàng Văn E', '123456785', 'Nam', '0909000005', '2025-01-05');

-- Booking_Ticket
INSERT INTO Booking_Ticket VALUES
-------- 35 chuyến bay từ 20/6 - 30/6/2025
('PDC0001', 'CB001', 'Lê Thị A', '259142893', 'Nữ', '0958895682', 'HV01', 1000000, '2025-06-18', FALSE, 'NV01'),
('PDC0002', 'CB001', 'Phan Ngọc', '970430275', 'Nữ', '0950935764', 'HV01', 1000000, '2025-06-18', FALSE, 'NV03'),
('PDC0003', 'CB001', 'Hoàng Mai', '696719126', 'Nữ', '0949679121', 'HV01', 1000000, '2025-06-18', TRUE, 'NV02'),
('PDC0004', 'CB001', 'Phan Bích', '914820005', 'Nữ', '0999946940', 'HV02', 1500000, '2025-06-18', FALSE, 'NV03'),
('PDC0005', 'CB002', 'Lê Linh', '646930224', 'Nữ', '0922213753', 'HV02', 1300000, '2025-06-19', TRUE, 'NV05'),
('PDC0006', 'CB002', 'Trần Diệu', '022831402', 'Nữ', '0916454623', 'HV02', 1300000, '2025-06-19', FALSE, 'NV02'),
('PDC0007', 'CB002', 'Võ Hằng', '106494565', 'Nữ', '0917808873', 'HV03', 1800000, '2025-06-19', FALSE, 'NV02'),
('PDC0008', 'CB003', 'Nguyễn Văn Giang', '117382178', 'Nam', '0905400573', 'HV01', 1100000, '2025-06-20', FALSE, 'NV02'),
('PDC0009', 'CB003', 'Võ Hải', '857927737', 'Nam', '0968797335', 'HV01', 1100000, '2025-06-20', TRUE, 'NV02'),
('PDC0010', 'CB004', 'Trần Khánh', '476347219', 'Nam', '0989737259', 'HV02', 1700000, '2025-06-21', TRUE, 'NV03'),
('PDC0011', 'CB004', 'Phan Diệu', '847831663', 'Nữ', '0957477508', 'HV02', 1700000, '2025-06-21', TRUE, 'NV03'),
('PDC0012', 'CB005', 'Trần Cảnh', '339097421', 'Nam', '0975200704', 'HV03', 1900000, '2025-06-22', TRUE, 'NV04'),
('PDC0013', 'CB006', 'Phạm Dũng', '568297102', 'Nam', '0939549498', 'HV01', 1150000, '2025-06-23', TRUE, 'NV02'),
('PDC0014', 'CB006', 'Trần Bình', '268368080', 'Nam', '0991818646', 'HV01', 1150000, '2025-06-23', TRUE, 'NV05'),
('PDC0015', 'CB006', 'Võ Khánh', '237678263', 'Nam', '0943512772', 'HV04', 2500000, '2025-06-23', TRUE, 'NV03'),
('PDC0016', 'CB006', 'Phan Minh', '631382428', 'Nam', '0959534086', 'HV04', 2500000, '2025-06-23', TRUE, 'NV05'),
('PDC0017', 'CB006', 'Huỳnh Ngọc', '953658497', 'Nữ', '0914218209', 'HV04', 2500000, '2025-06-23', TRUE, 'NV03'),
('PDC0018', 'CB007', 'Trần Minh', '854688682', 'Nam', '0995087414', 'HV02', 1350000, '2025-06-24', TRUE, 'NV02'),
('PDC0019', 'CB007', 'Phan Bình', '660904124', 'Nam', '0997545733', 'HV02', 1350000, '2025-06-24', TRUE, 'NV04'),
('PDC0020', 'CB008', 'Hoàng Hằng', '918822137', 'Nữ', '0983205337', 'HV02', 1400000, '2025-06-25', TRUE, 'NV01'),
('PDC0021', 'CB008', 'Lê Dũng', '087914319', 'Nam', '0990092768', 'HV02', 1400000, '2025-06-25', TRUE, 'NV05'),
('PDC0022', 'CB008', 'Phạm Bình', '159353896', 'Nam', '0939011507', 'HV02', 1400000, '2025-06-25', TRUE, 'NV01'),
('PDC0023', 'CB009', 'Võ Dũng', '467853020', 'Nam', '0982381186', 'HV01', 1000000, '2025-06-26', TRUE, 'NV04'),
('PDC0024', 'CB009', 'Phạm Cảnh', '346216990', 'Nam', '0993370273', 'HV01', 1000000, '2025-06-26', FALSE, 'NV02'),
('PDC0025', 'CB009', 'Nguyễn Văn Cảnh', '539602596', 'Nam', '0902255108', 'HV01', 1000000, '2025-06-26', FALSE, 'NV04'),
('PDC0026', 'CB009', 'Phạm Hằng', '941791587', 'Nữ', '0915351327', 'HV02', 1450000, '2025-06-26', FALSE, 'NV05'),
('PDC0027', 'CB010', 'Nguyễn Thị Diệu', '111258065', 'Nữ', '0961490705', 'HV01', 1050000, '2025-06-27', TRUE, 'NV02'),
('PDC0028', 'CB010', 'Lê An', '825828090', 'Nam', '0957885024', 'HV01', 1050000, '2025-06-27', FALSE, 'NV02'),
('PDC0029', 'CB010', 'Lê Hải', '407114342', 'Nam', '0937868598', 'HV03', 1750000, '2025-06-27', TRUE, 'NV05'),
('PDC0030', 'CB011', 'Phan Minh', '072470840', 'Nam', '0910544603', 'HV01', 950000, '2025-06-18', FALSE, 'NV02'),
('PDC0031', 'CB011', 'Nguyễn Thị Bích', '538214390', 'Nữ', '0966259669', 'HV01', 950000, '2025-06-18', FALSE, 'NV05'),
('PDC0032', 'CB011', 'Phan Cảnh', '813860869', 'Nam', '0918234861', 'HV01', 950000, '2025-06-18', TRUE, 'NV05'),
('PDC0033', 'CB012', 'Hoàng Dũng', '226158514', 'Nam', '0937968092', 'HV01', 1100000, '2025-06-19', TRUE, 'NV04'),
('PDC0034', 'CB012', 'Phan Bình', '733852816', 'Nam', '0983900519', 'HV01', 1100000, '2025-06-19', TRUE, 'NV05'),
('PDC0035', 'CB012', 'Phạm Giang', '357862125', 'Nam', '0910240862', 'HV02', 1600000, '2025-06-19', TRUE, 'NV01'),
('PDC0036', 'CB013', 'Lê Cảnh', '490847359', 'Nam', '0908114159', 'HV02', 1400000, '2025-06-20', FALSE, 'NV05'),
('PDC0037', 'CB013', 'Phạm Khánh', '564334020', 'Nam', '0956407398', 'HV02', 1400000, '2025-06-20', TRUE, 'NV03'),
('PDC0038', 'CB013', 'Hoàng Chi', '122952639', 'Nữ', '0970710131', 'HV02', 1400000, '2025-06-20', FALSE, 'NV03'),
('PDC0039', 'CB013', 'Trần Minh', '628915566', 'Nam', '0980431986', 'HV03', 2000000, '2025-06-20', FALSE, 'NV05'),
('PDC0040', 'CB014', 'Trần Dũng', '803346782', 'Nam', '0919820829', 'HV03', 2100000, '2025-06-21', FALSE, 'NV04'),
('PDC0041', 'CB015', 'Phan Mai', '499865041', 'Nữ', '0905045408', 'HV01', 1200000, '2025-06-22', FALSE, 'NV01'),
('PDC0042', 'CB015', 'Trần Hải', '577695646', 'Nam', '0905323205', 'HV01', 1200000, '2025-06-22', TRUE, 'NV02'),
('PDC0043', 'CB015', 'Huỳnh Cảnh', '531365135', 'Nam', '0957420041', 'HV01', 1200000, '2025-06-22', FALSE, 'NV01'),
('PDC0044', 'CB016', 'Hoàng Bình', '250383649', 'Nam', '0980228825', 'HV04', 2400000, '2025-06-23', TRUE, 'NV05'),
('PDC0045', 'CB016', 'Nguyễn Thị Bích', '222103713', 'Nữ', '0969113430', 'HV04', 2400000, '2025-06-23', TRUE, 'NV01'),
('PDC0046', 'CB017', 'Trần Mai', '959200298', 'Nữ', '0944799352', 'HV01', 1000000, '2025-06-24', TRUE, 'NV01'),
('PDC0047', 'CB018', 'Trần Minh', '351695100', 'Nam', '0936751995', 'HV02', 1350000, '2025-06-25', FALSE, 'NV04'),
('PDC0048', 'CB018', 'Huỳnh Minh', '240641389', 'Nam', '0907714116', 'HV03', 1850000, '2025-06-25', FALSE, 'NV05'),
('PDC0049', 'CB018', 'Trần Hằng', '546108868', 'Nữ', '0957921426', 'HV03', 1850000, '2025-06-25', TRUE, 'NV05'),
('PDC0050', 'CB018', 'Phan Hằng', '116296505', 'Nữ', '0945754870', 'HV03', 1850000, '2025-06-25', FALSE, 'NV01'),
('PDC0051', 'CB019', 'Huỳnh Khánh', '291074826', 'Nam', '0999290964', 'HV02', 1300000, '2025-06-26', TRUE, 'NV03'),
('PDC0052', 'CB019', 'Nguyễn Văn Bình', '032587338', 'Nam', '0934324041', 'HV02', 1300000, '2025-06-26', FALSE, 'NV04'),
('PDC0053', 'CB020', 'Trần Ngọc', '086740937', 'Nữ', '0935426088', 'HV03', 1850000, '2025-06-27', TRUE, 'NV03'),
('PDC0054', 'CB020', 'Nguyễn Văn Hải', '449643569', 'Nam', '0970096590', 'HV03', 1850000, '2025-06-27', TRUE, 'NV04'),
('PDC0055', 'CB020', 'Võ Anh', '967847662', 'Nữ', '0926347250', 'HV03', 1850000, '2025-06-27', FALSE, 'NV03'),
('PDC0056', 'CB021', 'Lê Thị A', '111111111', 'Nữ', '0912340001', 'HV01', 1000000, '2025-06-18', TRUE, 'NV01'),
('PDC0057', 'CB021', 'Nguyễn Văn B', '222222222', 'Nam', '0912340002', 'HV01', 1000000, '2025-06-18', FALSE, 'NV03'),
('PDC0058', 'CB021', 'Trần Thị C', '333333333', 'Nữ', '0912340003', 'HV01', 1000000, '2025-06-18', TRUE, 'NV05'),
('PDC0059', 'CB022', 'Phạm Văn D', '444444444', 'Nam', '0912340004', 'HV02', 1300000, '2025-06-19', TRUE, 'NV02'),
('PDC0060', 'CB022', 'Hoàng Thị E', '555555555', 'Nữ', '0912340005', 'HV03', 1800000, '2025-06-19', FALSE, 'NV04'),
('PDC0061', 'CB022', 'Vũ Văn F', '666666666', 'Nam', '0912340006', 'HV03', 1800000, '2025-06-19', TRUE, 'NV01'),
('PDC0062', 'CB023', 'Đặng Thị G', '777777777', 'Nữ', '0912340007', 'HV01', 1100000, '2025-06-20', FALSE, 'NV03'),
('PDC0063', 'CB023', 'Bùi Văn H', '888888888', 'Nam', '0912340008', 'HV01', 1100000, '2025-06-20', TRUE, 'NV05'),
('PDC0064', 'CB024', 'Lý Thị I', '999999999', 'Nữ', '0912340009', 'HV02', 1700000, '2025-06-21', TRUE, 'NV02'),
('PDC0065', 'CB025', 'Nguyễn Văn K', '010101010', 'Nam', '0912340010', 'HV03', 1900000, '2025-06-22', FALSE, 'NV04'),
('PDC0066', 'CB025', 'Trần Thị L', '020202020', 'Nữ', '0912340011', 'HV03', 1900000, '2025-06-22', TRUE, 'NV01'),
('PDC0067', 'CB025', 'Phạm Văn M', '030303030', 'Nam', '0912340012', 'HV03', 1900000, '2025-06-22', FALSE, 'NV03'),
('PDC0068', 'CB026', 'Hoàng Thị N', '040404040', 'Nữ', '0912340013', 'HV01', 1150000, '2025-06-23', TRUE, 'NV05'),
('PDC0069', 'CB026', 'Vũ Văn O', '050505050', 'Nam', '0912340014', 'HV01', 1150000, '2025-06-23', FALSE, 'NV02'),
('PDC0070', 'CB026', 'Đặng Thị P', '060606060', 'Nữ', '0912340015', 'HV01', 1150000, '2025-06-23', TRUE, 'NV04'),
('PDC0071', 'CB027', 'Bùi Văn Q', '070707070', 'Nam', '0912340016', 'HV02', 1350000, '2025-06-24', FALSE, 'NV01'),
('PDC0072', 'CB027', 'Lý Thị R', '080808080', 'Nữ', '0912340017', 'HV02', 1350000, '2025-06-24', TRUE, 'NV03'),
('PDC0073', 'CB028', 'Nguyễn Văn S', '090909090', 'Nam', '0912340018', 'HV02', 1400000, '2025-06-25', TRUE, 'NV05'),
('PDC0074', 'CB028', 'Trần Thị T', '101010101', 'Nữ', '0912340019', 'HV02', 1400000, '2025-06-25', FALSE, 'NV02'),
('PDC0075', 'CB028', 'Phạm Văn U', '111111111', 'Nam', '0912340020', 'HV03', 1950000, '2025-06-25', TRUE, 'NV04'),
('PDC0076', 'CB029', 'Hoàng Thị V', '121212121', 'Nữ', '0912340021', 'HV02', 1450000, '2025-06-26', FALSE, 'NV01'),
('PDC0077', 'CB029', 'Vũ Văn X', '131313131', 'Nam', '0912340022', 'HV02', 1450000, '2025-06-26', TRUE, 'NV03'),
('PDC0078', 'CB030', 'Đặng Thị Y', '141414141', 'Nữ', '0912340023', 'HV01', 1050000, '2025-06-27', TRUE, 'NV05'),
('PDC0079', 'CB030', 'Bùi Văn Z', '151515151', 'Nam', '0912340024', 'HV01', 1050000, '2025-06-27', FALSE, 'NV02'),
('PDC0080', 'CB030', 'Lý Thị AA', '161616161', 'Nữ', '0912340025', 'HV01', 1050000, '2025-06-27', TRUE, 'NV04'),
('PDC0081', 'CB031', 'Nguyễn Văn BB', '171717171', 'Nam', '0912340026', 'HV01', 950000, '2025-06-28', FALSE, 'NV01'),
('PDC0082', 'CB031', 'Trần Thị CC', '181818181', 'Nữ', '0912340027', 'HV01', 950000, '2025-06-28', TRUE, 'NV03'),
('PDC0083', 'CB032', 'Phạm Văn DD', '191919191', 'Nam', '0912340028', 'HV01', 1100000, '2025-06-28', TRUE, 'NV05'),
('PDC0084', 'CB033', 'Hoàng Thị EE', '202020202', 'Nữ', '0912340029', 'HV02', 1400000, '2025-06-28', FALSE, 'NV02'),
('PDC0085', 'CB033', 'Vũ Văn FF', '212121212', 'Nam', '0912340030', 'HV02', 1400000, '2025-06-28', TRUE, 'NV04'),
('PDC0086', 'CB033', 'Đặng Thị GG', '222222222', 'Nữ', '0912340031', 'HV02', 1400000, '2025-06-28', FALSE, 'NV01'),
('PDC0087', 'CB034', 'Bùi Văn HH', '232323232', 'Nam', '0912340032', 'HV03', 2100000, '2025-06-28', TRUE, 'NV03'),
('PDC0088', 'CB035', 'Lý Thị II', '242424242', 'Nữ', '0912340033', 'HV01', 1200000, '2025-06-28', FALSE, 'NV05'),
('PDC0089', 'CB035', 'Nguyễn Văn KK', '252525252', 'Nam', '0912340034', 'HV01', 1200000, '2025-06-28', TRUE, 'NV02'),

-------- 20 chuyến bay từ 1/6 - 19/6/2025
('PDC0090', 'CB036', 'Lê Văn B', '111111112', 'Nam', '0912340002', 'HV02', 1500000, '2025-05-30', TRUE, 'NV01'),
('PDC0091', 'CB036', 'Trần Thị C', '111111113', 'Nữ', '0912340003', 'HV02', 1500000, '2025-05-30', TRUE, 'NV05'),
('PDC0092', 'CB036', 'Nguyễn Văn D', '111111114', 'Nam', '0912340004', 'HV04', 2400000, '2025-05-30', TRUE, 'NV03'),
('PDC0093', 'CB036', 'Phạm Thị E', '111111115', 'Nữ', '0912340005', 'HV04', 2400000, '2025-05-30', TRUE, 'NV02'),
('PDC0094', 'CB037', 'Hoàng Văn F', '111111116', 'Nam', '0912340006', 'HV01', 1000000, '2025-05-31', TRUE, 'NV04'),
('PDC0095', 'CB037', 'Đặng Thị G', '111111117', 'Nữ', '0912340007', 'HV01', 1000000, '2025-05-31', TRUE, 'NV01'),
('PDC0096', 'CB037', 'Vũ Văn H', '111111118', 'Nam', '0912340008', 'HV01', 1000000, '2025-05-31', TRUE, 'NV03'),
('PDC0097', 'CB038', 'Bùi Thị I', '111111119', 'Nữ', '0912340009', 'HV02', 1350000, '2025-06-01', TRUE, 'NV02'),
('PDC0098', 'CB038', 'Lý Văn K', '111111120', 'Nam', '0912340010', 'HV02', 1350000, '2025-06-01', TRUE, 'NV05'),
('PDC0099', 'CB038', 'Mai Thị L', '111111121', 'Nữ', '0912340011', 'HV03', 1850000, '2025-06-01', TRUE, 'NV04'),
('PDC0100', 'CB038', 'Trần Văn M', '111111122', 'Nam', '0912340012', 'HV03', 1850000, '2025-06-01', TRUE, 'NV01'),
('PDC0101', 'CB039', 'Đỗ Thị N', '111111123', 'Nữ', '0912340013', 'HV02', 1300000, '2025-06-02', TRUE, 'NV03'),
('PDC0102', 'CB039', 'Phan Văn O', '111111124', 'Nam', '0912340014', 'HV02', 1300000, '2025-06-02', TRUE, 'NV02'),
('PDC0103', 'CB039', 'Dương Thị P', '111111125', 'Nữ', '0912340015', 'HV02', 1300000, '2025-06-02', TRUE, 'NV05'),
('PDC0104', 'CB040', 'Võ Văn Q', '111111126', 'Nam', '0912340016', 'HV01', 1350000, '2025-06-03', TRUE, 'NV04'),
('PDC0105', 'CB040', 'Lê Thị R', '111111127', 'Nữ', '0912340017', 'HV01', 1350000, '2025-06-03', TRUE, 'NV01'),
('PDC0106', 'CB040', 'Nguyễn Văn S', '111111128', 'Nam', '0912340018', 'HV03', 1850000, '2025-06-03', TRUE, 'NV03'),
('PDC0107', 'CB041', 'Trần Thị T', '111111129', 'Nữ', '0912340019', 'HV01', 1000000, '2025-06-04', TRUE, 'NV02'),
('PDC0108', 'CB041', 'Phạm Văn U', '111111130', 'Nam', '0912340020', 'HV01', 1000000, '2025-06-04', TRUE, 'NV05'),
('PDC0109', 'CB041', 'Hoàng Thị V', '111111131', 'Nữ', '0912340021', 'HV02', 1500000, '2025-06-04', TRUE, 'NV04'),
('PDC0110', 'CB042', 'Đặng Văn X', '111111132', 'Nam', '0912340022', 'HV02', 1300000, '2025-06-05', TRUE, 'NV01'),
('PDC0111', 'CB042', 'Vũ Thị Y', '111111133', 'Nữ', '0912340023', 'HV02', 1300000, '2025-06-05', TRUE, 'NV03'),
('PDC0112', 'CB042', 'Bùi Văn Z', '111111134', 'Nam', '0912340024', 'HV02', 1300000, '2025-06-05', TRUE, 'NV02'),
('PDC0113', 'CB043', 'Lý Thị A1', '111111135', 'Nữ', '0912340025', 'HV01', 1100000, '2025-06-06', TRUE, 'NV05'),
('PDC0114', 'CB044', 'Mai Văn B1', '111111136', 'Nam', '0912340026', 'HV01', 1200000, '2025-06-07', TRUE, 'NV04'),
('PDC0115', 'CB044', 'Trần Thị C1', '111111137', 'Nữ', '0912340027', 'HV01', 1200000, '2025-06-07', TRUE, 'NV01'),
('PDC0116', 'CB044', 'Đỗ Văn D1', '111111138', 'Nam', '0912340028', 'HV02', 1700000, '2025-06-07', TRUE, 'NV03'),
('PDC0117', 'CB044', 'Phan Thị E1', '111111139', 'Nữ', '0912340029', 'HV02', 1700000, '2025-06-07', TRUE, 'NV02'),
('PDC0118', 'CB045', 'Dương Văn F1', '111111140', 'Nam', '0912340030', 'HV03', 1900000, '2025-06-08', TRUE, 'NV05'),
('PDC0119', 'CB045', 'Võ Thị G1', '111111141', 'Nữ', '0912340031', 'HV03', 1900000, '2025-06-08', TRUE, 'NV04'),
('PDC0120', 'CB046', 'Lê Văn H1', '111111142', 'Nam', '0912340032', 'HV01', 1150000, '2025-06-09', TRUE, 'NV01'),
('PDC0121', 'CB046', 'Nguyễn Thị I1', '111111143', 'Nữ', '0912340033', 'HV01', 1150000, '2025-06-09', TRUE, 'NV03'),
('PDC0122', 'CB046', 'Trần Văn K1', '111111144', 'Nam', '0912340034', 'HV04', 2500000, '2025-06-09', TRUE, 'NV02'),
('PDC0123', 'CB047', 'Phạm Thị L1', '111111145', 'Nữ', '0912340035', 'HV02', 1350000, '2025-06-10', TRUE, 'NV05'),
('PDC0124', 'CB047', 'Hoàng Văn M1', '111111146', 'Nam', '0912340036', 'HV02', 1350000, '2025-06-10', TRUE, 'NV04'),
('PDC0125', 'CB048', 'Đặng Thị N1', '111111147', 'Nữ', '0912340037', 'HV02', 1400000, '2025-06-11', TRUE, 'NV01'),
('PDC0126', 'CB048', 'Vũ Văn O1', '111111148', 'Nam', '0912340038', 'HV02', 1400000, '2025-06-11', TRUE, 'NV03'),
('PDC0127', 'CB048', 'Bùi Thị P1', '111111149', 'Nữ', '0912340039', 'HV03', 1950000, '2025-06-11', TRUE, 'NV02'),
('PDC0128', 'CB048', 'Lý Văn Q1', '111111150', 'Nam', '0912340040', 'HV03', 1950000, '2025-06-11', TRUE, 'NV05'),
('PDC0129', 'CB049', 'Mai Thị R1', '111111151', 'Nữ', '0912340041', 'HV01', 1000000, '2025-06-12', TRUE, 'NV04'),
('PDC0130', 'CB049', 'Trần Văn S1', '111111152', 'Nam', '0912340042', 'HV01', 1000000, '2025-06-12', TRUE, 'NV01'),
('PDC0131', 'CB049', 'Đỗ Thị T1', '111111153', 'Nữ', '0912340043', 'HV01', 1000000, '2025-06-12', TRUE, 'NV03'),
('PDC0132', 'CB049', 'Phan Văn U1', '111111154', 'Nam', '0912340044', 'HV02', 1450000, '2025-06-12', TRUE, 'NV02'),
('PDC0133', 'CB050', 'Dương Thị V1', '111111155', 'Nữ', '0912340045', 'HV01', 1050000, '2025-06-13', TRUE, 'NV05'),
('PDC0134', 'CB050', 'Võ Văn X1', '111111156', 'Nam', '0912340046', 'HV01', 1050000, '2025-06-13', TRUE, 'NV04'),
('PDC0135', 'CB050', 'Lê Thị Y1', '111111157', 'Nữ', '0912340047', 'HV01', 1050000, '2025-06-13', TRUE, 'NV01'),
('PDC0136', 'CB050', 'Nguyễn Văn Z1', '111111158', 'Nam', '0912340048', 'HV03', 1750000, '2025-06-13', TRUE, 'NV03'),
('PDC0137', 'CB050', 'Trần Thị A2', '111111159', 'Nữ', '0912340049', 'HV03', 1750000, '2025-06-13', TRUE, 'NV02'),
('PDC0138', 'CB051', 'Phạm Văn B2', '111111160', 'Nam', '0912340050', 'HV01', 950000, '2025-06-14', TRUE, 'NV05'),
('PDC0139', 'CB051', 'Hoàng Thị C2', '111111161', 'Nữ', '0912340051', 'HV01', 950000, '2025-06-14', TRUE, 'NV04'),
('PDC0140', 'CB051', 'Đặng Văn D2', '111111162', 'Nam', '0912340052', 'HV01', 950000, '2025-06-14', TRUE, 'NV01'),
('PDC0141', 'CB052', 'Vũ Thị E2', '111111163', 'Nữ', '0912340053', 'HV01', 1100000, '2025-06-15', TRUE, 'NV03'),
('PDC0142', 'CB052', 'Bùi Văn F2', '111111164', 'Nam', '0912340054', 'HV01', 1100000, '2025-06-15', TRUE, 'NV02'),
('PDC0143', 'CB052', 'Lý Thị G2', '111111165', 'Nữ', '0912340055', 'HV01', 1100000, '2025-06-15', TRUE, 'NV05'),
('PDC0144', 'CB052', 'Mai Văn H2', '111111166', 'Nam', '0912340056', 'HV02', 1600000, '2025-06-15', TRUE, 'NV04'),
('PDC0145', 'CB052', 'Trần Thị I2', '111111167', 'Nữ', '0912340057', 'HV02', 1600000, '2025-06-15', TRUE, 'NV01'),
('PDC0146', 'CB053', 'Đỗ Văn K2', '111111168', 'Nam', '0912340058', 'HV02', 1400000, '2025-06-16', TRUE, 'NV03'),
('PDC0147', 'CB053', 'Phan Thị L2', '111111169', 'Nữ', '0912340059', 'HV03', 2000000, '2025-06-16', TRUE, 'NV02'),
('PDC0148', 'CB054', 'Dương Văn M2', '111111170', 'Nam', '0912340060', 'HV03', 2100000, '2025-06-17', TRUE, 'NV05'),
('PDC0149', 'CB055', 'Võ Thị N2', '111111171', 'Nữ', '0912340061', 'HV01', 1200000, '2025-06-17', TRUE, 'NV04'),
('PDC0150', 'CB055', 'Lê Văn O2', '111111172', 'Nam', '0912340062', 'HV01', 1200000, '2025-06-17', TRUE, 'NV02'),

---------- Tháng 1 – 5/2025 (25 chuyến)
('PDC0151', 'CB056', 'Nguyễn Thị Hương', '034293817', 'Nữ', '0912345678', 'HV02', 1500000, '2025-01-08', TRUE, 'NV01'),
('PDC0152', 'CB056', 'Trần Văn Long', '035628193', 'Nam', '0912345679', 'HV02', 1500000, '2025-01-08', TRUE, 'NV03'),
('PDC0153', 'CB056', 'Phạm Minh Đức', '036710294', 'Nam', '0912345680', 'HV04', 2400000, '2025-01-08', TRUE, 'NV05'),
('PDC0154', 'CB057', 'Lê Thị Mai', '037829305', 'Nữ', '0912345681', 'HV01', 1000000, '2025-01-13', TRUE, 'NV02'),
('PDC0155', 'CB057', 'Đỗ Văn Cường', '038930416', 'Nam', '0912345682', 'HV01', 1000000, '2025-01-13', TRUE, 'NV04'),
('PDC0156', 'CB057', 'Hoàng Thị Thoa', '039041527', 'Nữ', '0912345683', 'HV01', 1000000, '2025-01-13', TRUE, 'NV01'),
('PDC0157', 'CB058', 'Vũ Anh Tuấn', '040152638', 'Nam', '0912345684', 'HV02', 1350000, '2025-01-18', TRUE, 'NV03'),
('PDC0158', 'CB058', 'Nguyễn Thị Bích', '041263749', 'Nữ', '0912345685', 'HV02', 1350000, '2025-01-18', TRUE, 'NV05'),
('PDC0159', 'CB058', 'Trần Đình Trung', '042374850', 'Nam', '0912345686', 'HV02', 1350000, '2025-01-18', TRUE, 'NV02'),
('PDC0160', 'CB059', 'Phạm Thị Lan', '043485961', 'Nữ', '0912345687', 'HV02', 1300000, '2025-01-23', TRUE, 'NV04'),
('PDC0161', 'CB060', 'Lê Văn Khải', '044596072', 'Nam', '0912345688', 'HV03', 1850000, '2025-01-28', TRUE, 'NV01'),
('PDC0162', 'CB060', 'Đỗ Thị Minh', '045607183', 'Nữ', '0912345689', 'HV03', 1850000, '2025-01-28', TRUE, 'NV03'),
('PDC0163', 'CB061', 'Hoàng Anh Khoa', '046718294', 'Nam', '0912345690', 'HV01', 1000000, '2025-02-08', TRUE, 'NV05'),
('PDC0164', 'CB061', 'Vũ Thị Hồng', '047829305', 'Nữ', '0912345691', 'HV01', 1000000, '2025-02-08', TRUE, 'NV02'),
('PDC0165', 'CB062', 'Nguyễn Văn Nam', '048930416', 'Nam', '0912345692', 'HV03', 1800000, '2025-02-13', TRUE, 'NV04'),
('PDC0166', 'CB063', 'Trần Thị Hằng', '049041527', 'Nữ', '0912345693', 'HV01', 1100000, '2025-02-18', TRUE, 'NV01'),
('PDC0167', 'CB063', 'Phạm Văn Hùng', '050152638', 'Nam', '0912345694', 'HV01', 1100000, '2025-02-18', TRUE, 'NV03'),
('PDC0168', 'CB064', 'Lê Minh Thảo', '051263749', 'Nữ', '0912345695', 'HV02', 1700000, '2025-02-23', TRUE, 'NV05'),
('PDC0169', 'CB064', 'Đỗ Anh Dũng', '052374850', 'Nam', '0912345696', 'HV02', 1700000, '2025-02-23', TRUE, 'NV02'),
('PDC0170', 'CB065', 'Hoàng Thị Trâm', '053485961', 'Nữ', '0912345697', 'HV03', 1900000, '2025-02-26', TRUE, 'NV04'),
('PDC0171', 'CB066', 'Vũ Minh Quân', '054596072', 'Nam', '0912345698', 'HV01', 1150000, '2025-03-03', TRUE, 'NV01'),
('PDC0172', 'CB066', 'Nguyễn Thu Phương', '055607183', 'Nữ', '0912345699', 'HV01', 1150000, '2025-03-03', TRUE, 'NV03'),
('PDC0173', 'CB066', 'Trần Văn Tùng', '056718294', 'Nam', '0912345700', 'HV04', 2500000, '2025-03-03', TRUE, 'NV05'),
('PDC0174', 'CB066', 'Phạm Thị Thúy', '057829305', 'Nữ', '0912345701', 'HV04', 2500000, '2025-03-03', TRUE, 'NV02'),
('PDC0175', 'CB067', 'Lê Văn Quyết', '058930416', 'Nam', '0912345702', 'HV02', 1350000, '2025-03-08', TRUE, 'NV04'),
('PDC0176', 'CB067', 'Đỗ Thị Loan', '059041527', 'Nữ', '0912345703', 'HV02', 1350000, '2025-03-08', TRUE, 'NV01'),
('PDC0177', 'CB067', 'Hoàng Gia Bảo', '060152638', 'Nam', '0912345704', 'HV02', 1350000, '2025-03-08', TRUE, 'NV03'),
('PDC0178', 'CB068', 'Vũ Thị Kim', '061263749', 'Nữ', '0912345705', 'HV02', 1400000, '2025-03-13', TRUE, 'NV05'),
('PDC0179', 'CB068', 'Nguyễn Thanh Tùng', '062374850', 'Nam', '0912345706', 'HV02', 1400000, '2025-03-13', TRUE, 'NV02'),
('PDC0180', 'CB068', 'Trần Thị Diệu', '063485961', 'Nữ', '0912345707', 'HV03', 1950000, '2025-03-13', TRUE, 'NV04'),
('PDC0181', 'CB068', 'Phạm Văn Thành', '064596072', 'Nam', '0912345708', 'HV03', 1950000, '2025-03-13', TRUE, 'NV01'),
('PDC0182', 'CB069', 'Lê Thị Ngọc', '065607183', 'Nữ', '0912345709', 'HV01', 1000000, '2025-03-18', TRUE, 'NV03'),
('PDC0183', 'CB069', 'Đỗ Minh Khang', '066718294', 'Nam', '0912345710', 'HV01', 1000000, '2025-03-18', TRUE, 'NV05'),
('PDC0184', 'CB069', 'Hoàng Văn Vinh', '067829305', 'Nam', '0912345711', 'HV02', 1450000, '2025-03-18', TRUE, 'NV02'),
('PDC0185', 'CB069', 'Vũ Thị Hường', '068930416', 'Nữ', '0912345712', 'HV02', 1450000, '2025-03-18', TRUE, 'NV04'),
('PDC0186', 'CB070', 'Nguyễn Đức Anh', '069041527', 'Nam', '0912345713', 'HV03', 1750000, '2025-03-23', TRUE, 'NV01'),
('PDC0187', 'CB070', 'Trần Thị Trang', '070152638', 'Nữ', '0912345714', 'HV03', 1750000, '2025-03-23', TRUE, 'NV03'),
('PDC0188', 'CB070', 'Phạm Văn Lâm', '071263749', 'Nam', '0912345715', 'HV01', 1050000, '2025-03-23', TRUE, 'NV05'),
('PDC0189', 'CB071', 'Lê Thị Thu', '072374850', 'Nữ', '0912345716', 'HV01', 950000, '2025-04-03', TRUE, 'NV02'),
('PDC0190', 'CB071', 'Đỗ Văn Sơn', '073485961', 'Nam', '0912345717', 'HV01', 950000, '2025-04-03', TRUE, 'NV04'),
('PDC0191', 'CB072', 'Hoàng Thị Vân', '074596072', 'Nữ', '0912345718', 'HV02', 1600000, '2025-04-08', TRUE, 'NV01'),
('PDC0192', 'CB072', 'Vũ Minh Trí', '075607183', 'Nam', '0912345719', 'HV02', 1600000, '2025-04-08', TRUE, 'NV03'),
('PDC0193', 'CB073', 'Nguyễn Thị Oanh', '076718294', 'Nữ', '0912345720', 'HV02', 1400000, '2025-04-13', TRUE, 'NV05'),
('PDC0194', 'CB075', 'Lê Thị Yến', '077829305', 'Nữ', '0912345721', 'HV01', 1200000, '2025-04-23', TRUE, 'NV02'),
('PDC0195', 'CB075', 'Đỗ Văn Phúc', '078930416', 'Nam', '0912345722', 'HV01', 1200000, '2025-04-23', TRUE, 'NV04'),
('PDC0196', 'CB076', 'Hoàng Thị Dung', '079041527', 'Nữ', '0912345723', 'HV02', 1500000, '2025-04-29', TRUE, 'NV01'),
('PDC0197', 'CB078', 'Vũ Văn Long', '080152638', 'Nam', '0912345724', 'HV03', 1850000, '2025-05-08', TRUE, 'NV03'),
('PDC0198', 'CB078', 'Nguyễn Thị Loan', '081263749', 'Nữ', '0912345725', 'HV03', 1850000, '2025-05-08', TRUE, 'NV05'),
('PDC0199', 'CB078', 'Trần Đình Quân', '082374850', 'Nam', '0912345726', 'HV02', 1350000, '2025-05-08', TRUE, 'NV02'),
('PDC0200', 'CB078', 'Phạm Thị Hương', '083485961', 'Nữ', '0912345727', 'HV02', 1350000, '2025-05-08', TRUE, 'NV04'),
('PDC0201', 'CB079', 'Lê Văn Hiếu', '084596072', 'Nam', '0912345728', 'HV02', 1300000, '2025-05-13', TRUE, 'NV01'),
('PDC0202', 'CB079', 'Đỗ Thị Thanh', '085607183', 'Nữ', '0912345729', 'HV02', 1300000, '2025-05-13', TRUE, 'NV03'),
('PDC0203', 'CB080', 'Hoàng Văn Khang', '086718294', 'Nam', '0912345730', 'HV03', 1850000, '2025-05-18', TRUE, 'NV05'),
('PDC0204', 'CB080', 'Vũ Thị Mai', '087829305', 'Nữ', '0912345731', 'HV03', 1850000, '2025-05-18', TRUE, 'NV02'),
('PDC0205', 'CB080', 'Nguyễn Văn Mạnh', '088930416', 'Nam', '0912345732', 'HV01', 1350000, '2025-05-18', TRUE, 'NV04'),
('PDC0206', 'CB080', 'Trần Thị Thu', '089041527', 'Nữ', '0912345733', 'HV01', 1350000, '2025-05-18', TRUE, 'NV01'),

----- 20 chuyến bay năm 2024 
('PDC0207', 'CB081', 'Trần Văn A', '111222333', 'Nam', '0912345678', 'HV01', 1000000, '2024-01-08', TRUE, 'NV01'),
('PDC0208', 'CB081', 'Nguyễn Thị B', '111222334', 'Nữ', '0912345679', 'HV01', 1000000, '2024-01-08', TRUE, 'NV02'),
('PDC0209', 'CB081', 'Phạm Văn C', '111222335', 'Nam', '0912345680', 'HV02', 1500000, '2024-01-08', TRUE, 'NV03'),
('PDC0210', 'CB082', 'Lê Thị D', '111222336', 'Nữ', '0912345681', 'HV02', 1300000, '2024-02-13', TRUE, 'NV04'),
('PDC0211', 'CB082', 'Hoàng Văn E', '111222337', 'Nam', '0912345682', 'HV02', 1300000, '2024-02-13', TRUE, 'NV05'),
('PDC0212', 'CB083', 'Đỗ Thị F', '111222338', 'Nữ', '0912345683', 'HV01', 1100000, '2024-03-18', TRUE, 'NV01'),
('PDC0213', 'CB084', 'Vũ Văn G', '111222339', 'Nam', '0912345684', 'HV01', 1200000, '2024-04-23', TRUE, 'NV02'),
('PDC0214', 'CB084', 'Bùi Thị H', '111222340', 'Nữ', '0912345685', 'HV01', 1200000, '2024-04-23', TRUE, 'NV03'),
('PDC0215', 'CB084', 'Trần Văn I', '111222341', 'Nam', '0912345686', 'HV01', 1200000, '2024-04-23', TRUE, 'NV04'),
('PDC0216', 'CB084', 'Nguyễn Thị J', '111222342', 'Nữ', '0912345687', 'HV02', 1700000, '2024-04-23', TRUE, 'NV05'),
('PDC0217', 'CB084', 'Phạm Văn K', '111222343', 'Nam', '0912345688', 'HV02', 1700000, '2024-04-23', TRUE, 'NV01'),
('PDC0218', 'CB085', 'Lê Thị L', '111222344', 'Nữ', '0912345689', 'HV03', 1900000, '2024-05-28', TRUE, 'NV02'),
('PDC0219', 'CB085', 'Hoàng Văn M', '111222345', 'Nam', '0912345690', 'HV03', 1900000, '2024-05-28', TRUE, 'NV03'),
('PDC0220', 'CB086', 'Đỗ Thị N', '111222346', 'Nữ', '0912345691', 'HV04', 2500000, '2024-06-03', TRUE, 'NV04'),
('PDC0221', 'CB086', 'Vũ Văn O', '111222347', 'Nam', '0912345692', 'HV04', 2500000, '2024-06-03', TRUE, 'NV05'),
('PDC0222', 'CB087', 'Bùi Thị P', '111222348', 'Nữ', '0912345693', 'HV02', 1350000, '2024-07-08', TRUE, 'NV01'),
('PDC0223', 'CB088', 'Trần Văn Q', '111222349', 'Nam', '0912345694', 'HV03', 1950000, '2024-08-13', TRUE, 'NV02'),
('PDC0224', 'CB088', 'Nguyễn Thị R', '111222350', 'Nữ', '0912345695', 'HV03', 1950000, '2024-08-13', TRUE, 'NV03'),
('PDC0225', 'CB089', 'Phạm Văn S', '111222351', 'Nam', '0912345696', 'HV02', 1450000, '2024-09-18', TRUE, 'NV04'),
('PDC0226', 'CB089', 'Lê Thị T', '111222352', 'Nữ', '0912345697', 'HV02', 1450000, '2024-09-18', TRUE, 'NV05'),
('PDC0227', 'CB089', 'Hoàng Văn U', '111222353', 'Nam', '0912345698', 'HV02', 1450000, '2024-09-18', TRUE, 'NV01'),
('PDC0228', 'CB090', 'Đỗ Thị V', '111222354', 'Nữ', '0912345699', 'HV01', 1050000, '2024-10-23', TRUE, 'NV02'),
('PDC0229', 'CB090', 'Vũ Văn W', '111222355', 'Nam', '0912345700', 'HV01', 1050000, '2024-10-23', TRUE, 'NV03'),
('PDC0230', 'CB091', 'Bùi Thị X', '111222356', 'Nữ', '0912345701', 'HV01', 950000, '2024-11-08', TRUE, 'NV04'),
('PDC0231', 'CB091', 'Trần Văn Y', '111222357', 'Nam', '0912345702', 'HV01', 950000, '2024-11-08', TRUE, 'NV05'),
('PDC0232', 'CB092', 'Nguyễn Thị Z', '111222358', 'Nữ', '0912345703', 'HV01', 1100000, '2024-12-13', TRUE, 'NV01'),
('PDC0233', 'CB093', 'Phạm Văn AA', '111222359', 'Nam', '0912345704', 'HV03', 2000000, '2024-01-18', TRUE, 'NV02'),
('PDC0234', 'CB093', 'Lê Thị BB', '111222360', 'Nữ', '0912345705', 'HV03', 2000000, '2024-01-18', TRUE, 'NV03'),
('PDC0235', 'CB094', 'Hoàng Văn CC', '111222361', 'Nam', '0912345706', 'HV03', 2100000, '2024-02-23', TRUE, 'NV04'),
('PDC0236', 'CB094', 'Đỗ Thị DD', '111222362', 'Nữ', '0912345707', 'HV03', 2100000, '2024-02-23', TRUE, 'NV05'),
('PDC0237', 'CB094', 'Vũ Văn EE', '111222363', 'Nam', '0912345708', 'HV03', 2100000, '2024-02-23', TRUE, 'NV01'),
('PDC0238', 'CB095', 'Bùi Thị FF', '111222364', 'Nữ', '0912345709', 'HV01', 1200000, '2024-03-28', TRUE, 'NV02'),
('PDC0239', 'CB095', 'Trần Văn GG', '111222365', 'Nam', '0912345710', 'HV01', 1200000, '2024-03-28', TRUE, 'NV03'),
('PDC0240', 'CB096', 'Nguyễn Thị HH', '111222366', 'Nữ', '0912345711', 'HV04', 2400000, '2024-04-03', TRUE, 'NV04'),
('PDC0241', 'CB096', 'Phạm Văn II', '111222367', 'Nam', '0912345712', 'HV04', 2400000, '2024-04-03', TRUE, 'NV05'),
('PDC0242', 'CB097', 'Lê Thị JJ', '111222368', 'Nữ', '0912345713', 'HV01', 1000000, '2024-05-08', TRUE, 'NV01'),
('PDC0243', 'CB097', 'Hoàng Văn KK', '111222369', 'Nam', '0912345714', 'HV01', 1000000, '2024-05-08', TRUE, 'NV02'),
('PDC0244', 'CB098', 'Đỗ Thị LL', '111222370', 'Nữ', '0912345715', 'HV02', 1350000, '2024-06-13', TRUE, 'NV03'),
('PDC0245', 'CB098', 'Vũ Văn MM', '111222371', 'Nam', '0912345716', 'HV02', 1350000, '2024-06-13', TRUE, 'NV04'),
('PDC0246', 'CB098', 'Bùi Thị NN', '111222372', 'Nữ', '0912345717', 'HV02', 1350000, '2024-06-13', TRUE, 'NV05'),
('PDC0247', 'CB099', 'Trần Văn OO', '111222373', 'Nam', '0912345718', 'HV02', 1300000, '2024-07-18', TRUE, 'NV01'),
('PDC0248', 'CB099', 'Nguyễn Thị PP', '111222374', 'Nữ', '0912345719', 'HV02', 1300000, '2024-07-18', TRUE, 'NV02'),
('PDC0249', 'CB100', 'Phạm Văn QQ', '111222375', 'Nam', '0912345720', 'HV01', 1350000, '2024-08-23', TRUE, 'NV03'),

----- 20 chuyến bay năm 2023
('PDC0250', 'CB101', 'Nguyễn Thị Hương', '012345678912', 'Nữ', '0901234567', 'HV01', 1000000, '2023-01-03', TRUE, 'NV01'),
('PDC0251', 'CB101', 'Trần Văn Tùng', '012345678913', 'Nam', '0901234568', 'HV01', 1000000, '2023-01-03', TRUE, 'NV02'),
('PDC0252', 'CB101', 'Lê Thu Thủy', '012345678914', 'Nữ', '0901234569', 'HV02', 1500000, '2023-01-03', TRUE, 'NV03'),
('PDC0253', 'CB101', 'Phạm Minh Đức', '012345678915', 'Nam', '0901234570', 'HV02', 1500000, '2023-01-03', TRUE, 'NV04'),
('PDC0254', 'CB101', 'Hoàng Ngọc Ánh', '012345678916', 'Nữ', '0901234571', 'HV02', 1500000, '2023-01-03', TRUE, 'NV05'),
('PDC0255', 'CB102', 'Vũ Anh Khoa', '012345678917', 'Nam', '0901234572', 'HV02', 1300000, '2023-02-08', TRUE, 'NV01'),
('PDC0256', 'CB103', 'Đặng Thúy Nga', '012345678918', 'Nữ', '0901234573', 'HV01', 1100000, '2023-03-13', TRUE, 'NV02'),
('PDC0257', 'CB103', 'Bùi Trung Kiên', '012345678919', 'Nam', '0901234574', 'HV01', 1100000, '2023-03-13', TRUE, 'NV03'),
('PDC0258', 'CB103', 'Ngô Lan Anh', '012345678920', 'Nữ', '0901234575', 'HV01', 1100000, '2023-03-13', TRUE, 'NV04'),
('PDC0259', 'CB104', 'Dương Quốc Việt', '012345678921', 'Nam', '0901234576', 'HV01', 1200000, '2023-04-18', TRUE, 'NV05'),
('PDC0260', 'CB104', 'Lê Thanh Bình', '012345678922', 'Nam', '0901234577', 'HV01', 1200000, '2023-04-18', TRUE, 'NV01'),
('PDC0261', 'CB104', 'Trần Thị Mai', '012345678923', 'Nữ', '0901234578', 'HV02', 1700000, '2023-04-18', TRUE, 'NV02'),
('PDC0262', 'CB104', 'Hoàng Gia Huy', '012345678924', 'Nam', '0901234579', 'HV02', 1700000, '2023-04-18', TRUE, 'NV03'),
('PDC0263', 'CB106', 'Phạm Thị Lan', '012345678925', 'Nữ', '0901234580', 'HV01', 1150000, '2023-06-28', TRUE, 'NV04'),
('PDC0264', 'CB106', 'Nguyễn Đức Thắng', '012345678926', 'Nam', '0901234581', 'HV01', 1150000, '2023-06-28', TRUE, 'NV05'),
('PDC0265', 'CB107', 'Đỗ Hải Yến', '012345678927', 'Nữ', '0901234582', 'HV02', 1350000, '2023-07-03', TRUE, 'NV01'),
('PDC0266', 'CB108', 'Nguyễn Thị Hoa', '012345678928', 'Nữ', '0901234583', 'HV02', 1400000, '2023-08-08', TRUE, 'NV02'),
('PDC0267', 'CB108', 'Trần Đình Nam', '012345678929', 'Nam', '0901234584', 'HV02', 1400000, '2023-08-08', TRUE, 'NV03'),
('PDC0268', 'CB108', 'Lý Kim Chi', '012345678930', 'Nữ', '0901234585', 'HV03', 1950000, '2023-08-08', TRUE, 'NV04'),
('PDC0269', 'CB108', 'Võ Thành Công', '012345678931', 'Nam', '0901234586', 'HV03', 1950000, '2023-08-08', TRUE, 'NV05'),
('PDC0270', 'CB108', 'Bùi Bích Ngọc', '012345678932', 'Nữ', '0901234587', 'HV03', 1950000, '2023-08-08', TRUE, 'NV01'),
('PDC0271', 'CB109', 'Nguyễn Hồng Minh', '012345678933', 'Nữ', '0901234588', 'HV02', 1450000, '2023-09-13', TRUE, 'NV02'),
('PDC0272', 'CB109', 'Lê Văn Hiếu', '012345678934', 'Nam', '0901234589', 'HV02', 1450000, '2023-09-13', TRUE, 'NV03'),
('PDC0273', 'CB110', 'Trần Minh Anh', '012345678935', 'Nữ', '0901234590', 'HV03', 1750000, '2023-10-18', TRUE, 'NV04'),
('PDC0274', 'CB110', 'Phạm Quốc An', '012345678936', 'Nam', '0901234591', 'HV03', 1750000, '2023-10-18', TRUE, 'NV05'),
('PDC0275', 'CB111', 'Đỗ Thị Quyên', '012345678937', 'Nữ', '0901234592', 'HV01', 950000, '2023-11-23', TRUE, 'NV01'),
('PDC0276', 'CB111', 'Hoàng Văn Lộc', '012345678938', 'Nam', '0901234593', 'HV01', 950000, '2023-11-23', TRUE, 'NV02'),
('PDC0277', 'CB111', 'Nguyễn Thị Bích', '012345678939', 'Nữ', '0901234594', 'HV01', 950000, '2023-11-23', TRUE, 'NV03'),
('PDC0278', 'CB112', 'Lê Hữu Nghĩa', '012345678940', 'Nam', '0901234595', 'HV01', 1100000, '2023-12-28', TRUE, 'NV04'),
('PDC0279', 'CB112', 'Vũ Thị Thanh', '012345678941', 'Nữ', '0901234596', 'HV01', 1100000, '2023-12-28', TRUE, 'NV05'),
('PDC0280', 'CB112', 'Trần Quang Vinh', '012345678942', 'Nam', '0901234597', 'HV02', 1600000, '2023-12-28', TRUE, 'NV01'),
('PDC0281', 'CB112', 'Phạm Gia Linh', '012345678943', 'Nữ', '0901234598', 'HV02', 1600000, '2023-12-28', TRUE, 'NV02'),
('PDC0282', 'CB112', 'Đào Duy Anh', '012345678944', 'Nam', '0901234599', 'HV02', 1600000, '2023-12-28', TRUE, 'NV03'),
('PDC0283', 'CB113', 'Nguyễn Thành Đạt', '012345678945', 'Nam', '0901234600', 'HV02', 1400000, '2023-02-27', TRUE, 'NV04'),
('PDC0284', 'CB113', 'Lê Thị Mai', '012345678946', 'Nữ', '0901234601', 'HV02', 1400000, '2023-02-27', TRUE, 'NV05'),
('PDC0285', 'CB113', 'Hoàng Văn Cường', '012345678947', 'Nam', '0901234602', 'HV02', 1400000, '2023-02-27', TRUE, 'NV01'),
('PDC0286', 'CB113', 'Trần Hữu Phúc', '012345678948', 'Nam', '0901234603', 'HV03', 2000000, '2023-02-27', TRUE, 'NV02'),
('PDC0287', 'CB114', 'Phạm Thị Thảo', '012345678949', 'Nữ', '0901234604', 'HV03', 2100000, '2023-04-29', TRUE, 'NV03'),
('PDC0288', 'CB114', 'Nguyễn Minh Quân', '012345678950', 'Nam', '0901234605', 'HV03', 2100000, '2023-04-29', TRUE, 'NV04'),
('PDC0289', 'CB116', 'Lê Thị Yến', '012345678951', 'Nữ', '0901234606', 'HV02', 1500000, '2023-08-30', TRUE, 'NV05'),
('PDC0290', 'CB116', 'Hoàng Bá Long', '012345678952', 'Nam', '0901234607', 'HV02', 1500000, '2023-08-30', TRUE, 'NV01'),
('PDC0291', 'CB116', 'Trần Ngọc Bích', '012345678953', 'Nữ', '0901234608', 'HV02', 1500000, '2023-08-30', TRUE, 'NV02'),
('PDC0292', 'CB116', 'Võ Mạnh Hùng', '012345678954', 'Nam', '0901234609', 'HV04', 2400000, '2023-08-30', TRUE, 'NV03'),
('PDC0293', 'CB116', 'Đắng Kim Ngân', '012345678955', 'Nữ', '0901234610', 'HV04', 2400000, '2023-08-30', TRUE, 'NV04'),
('PDC0294', 'CB117', 'Bùi Thanh Duy', '012345678956', 'Nam', '0901234611', 'HV01', 1000000, '2023-10-30', TRUE, 'NV05'),
('PDC0295', 'CB117', 'Nguyễn Thị Ánh', '012345678957', 'Nữ', '0901234612', 'HV01', 1000000, '2023-10-30', TRUE, 'NV01'),
('PDC0296', 'CB117', 'Trần Minh Thắng', '012345678958', 'Nam', '0901234613', 'HV01', 1000000, '2023-10-30', TRUE, 'NV02'),
('PDC0297', 'CB118', 'Lê Xuân Trường', '012345678959', 'Nam', '0901234614', 'HV02', 1350000, '2023-01-13', TRUE, 'NV03'),
('PDC0298', 'CB118', 'Phạm Thanh Vân', '012345678960', 'Nữ', '0901234615', 'HV02', 1350000, '2023-01-13', TRUE, 'NV04'),
('PDC0299', 'CB118', 'Nguyễn Văn Tiến', '012345678961', 'Nam', '0901234616', 'HV03', 1850000, '2023-01-13', TRUE, 'NV05'),
('PDC0300', 'CB120', 'Hoàng Văn Nam', '012345678962', 'Nam', '0901234617', 'HV01', 1350000, '2023-08-13', TRUE, 'NV01'),
('PDC0301', 'CB120', 'Lý Thị Kiều', '012345678963', 'Nữ', '0901234618', 'HV01', 1350000, '2023-08-13', TRUE, 'NV02');
