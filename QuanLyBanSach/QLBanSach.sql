create database QLCHBANSACH;
USE [QLCHBANSACH];
GO
/****** Object:  Table [dbo].[Bill]    Script Date: 06/14/2023 2:30:01 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Bill](
	[theloai] [nvarchar](20) NULL,
	[tensach] [nvarchar](20) NULL,
	[soluong] [int] NULL,
	[thanhtien] [int] NULL,
	[ngaymua] [date] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[KhoSach]    Script Date: 06/14/2023 2:30:01 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[KhoSach](
	[theloai] [nvarchar](20) NULL,
	[tensach] [nvarchar](20) NOT NULL,
	[tacgia] [nvarchar](20) NULL,
	[nxb] [nvarchar](20) NULL,
	[soluong] [int] NULL,
	[giatien] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[tensach] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
INSERT [dbo].[Bill] ([theloai], [tensach], [soluong], [thanhtien], [ngaymua]) VALUES (N'Tieu Thuyet', N'Luoc Su Thoi Gian', 4, 72000, CAST(N'2023-06-13' AS Date))
INSERT [dbo].[Bill] ([theloai], [tensach], [soluong], [thanhtien], [ngaymua]) VALUES (N'Cuoc Song', N'Cuoc Song Muon Mau', 2, 84000, CAST(N'2023-06-11' AS Date))
GO
INSERT [dbo].[KhoSach] ([theloai], [tensach], [tacgia], [nxb], [soluong], [giatien]) VALUES (N'Cuoc Song', N'Cuoc Song Muon Mau', N'Andrew', N'Ha Noi', 16, 42000)
INSERT [dbo].[KhoSach] ([theloai], [tensach], [tacgia], [nxb], [soluong], [giatien]) VALUES (N'Cuoc Song', N'Cuon Theo Chieu Gio', N'Margaret Munnerlyn', N'Kim Dong', 7, 15000)
INSERT [dbo].[KhoSach] ([theloai], [tensach], [tacgia], [nxb], [soluong], [giatien]) VALUES (N'Thieu Nhi', N'Doraemon', N'Fujiko Fujio', N'Kim DOng', 15, 25000)
INSERT [dbo].[KhoSach] ([theloai], [tensach], [tacgia], [nxb], [soluong], [giatien]) VALUES (N'Tieu Thuyet', N'Luoc Su Thoi Gian', N'Stephen Hawking', N'Hoa Hoc Tro', 0, 18000)
INSERT [dbo].[KhoSach] ([theloai], [tensach], [tacgia], [nxb], [soluong], [giatien]) VALUES (N'Tieu Thuyet', N'Nha Gia Kim', N'Paulo Coelho', N'Ha Noi', 10, 30000)
GO
ALTER TABLE [dbo].[Bill]  WITH CHECK ADD  CONSTRAINT [fk_htk_theloai] FOREIGN KEY([tensach])
REFERENCES [dbo].[KhoSach] ([tensach])
GO
ALTER TABLE [dbo].[Bill] CHECK CONSTRAINT [fk_htk_theloai]
GO
