using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Data.SqlClient;
using System.Data.SqlTypes;
using System.Data.Common;

namespace QLBanSach
{
    
    public partial class Form1 : Form
    {
        string strCon = @"Data Source=NV\SQLEXPRESS;Initial Catalog=QLCHBANSACH;Integrated Security=True;Encrypt=False";
        SqlConnection sqlCon = null;
        DateTime myDateVariable;
        public Form1()
        {
            InitializeComponent();
        }

        private void tabPage4_Click(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {
            hienthidanhsach();
            hienthidanhsachbuy();
        }

        private void hienthidanhsach()
        {
            sqlCon = new SqlConnection(strCon);
            sqlCon.Open();

            SqlCommand sqlCmd = new SqlCommand();
            sqlCmd.CommandType = CommandType.Text;
            sqlCmd.CommandText = "select * from KhoSach";
            sqlCmd.Connection = sqlCon;

            SqlDataReader reader = sqlCmd.ExecuteReader();
            while (reader.Read())
            {
                DataGridViewRow row = (DataGridViewRow)DTGRV1.Rows[0].Clone();
                //lay ra giá trị sql ->>> datagridview
                row.Cells[0].Value = reader.GetString(0);
                row.Cells[1].Value = reader.GetString(1);
                row.Cells[2].Value = reader.GetString(2);
                row.Cells[3].Value = reader.GetString(3);
                row.Cells[4].Value = reader.GetInt32(4);
                row.Cells[5].Value = reader.GetInt32(5);

                DTGRV1.Rows.Add(row);
            }
            reader.Close();

        }

        private void hienthidanhsachbuy()
        {
            sqlCon = new SqlConnection(strCon);
            sqlCon.Open();
            SqlCommand sqlCmd = new SqlCommand();
            sqlCmd.CommandType = CommandType.Text;
            sqlCmd.CommandText = "select * from Bill";
            sqlCmd.Connection = sqlCon;
            SqlDataReader reader2 = sqlCmd.ExecuteReader();
            while (reader2.Read())
            {
                DataGridViewRow row = (DataGridViewRow)DTGRV2.Rows[0].Clone();
                row.Cells[0].Value = reader2.GetString(0);
                row.Cells[1].Value = reader2.GetString(1);
                row.Cells[2].Value = reader2.GetInt32(2);
                row.Cells[3].Value = reader2.GetInt32(3);
                row.Cells[4].Value = reader2.GetDateTime(4).ToString().Substring(0, 10);

                DTGRV2.Rows.Add(row);
            }
        }
        private void btnBUYMua_Click(object sender, EventArgs e)
        {
            int slsql = 0;
            int txtsl = Convert.ToInt32(txtBUYSoLuong.Text);
            int soluongsaukhimua = 0;
            int thanhtien = txtsl * Convert.ToInt32(txtBUYGiaTien.Text);
            sqlCon = new SqlConnection(strCon);
            sqlCon.Open();
            DTGRV2.Rows.Clear();
            SqlCommand sqlCmd = new SqlCommand();
            sqlCmd.CommandType= CommandType.Text;
            sqlCmd.CommandText = "select soluong from KhoSach where tensach='"+txtBUYTenSach.Text+"'";
            sqlCmd.Connection = sqlCon;
            SqlDataReader reader = sqlCmd.ExecuteReader();
            while (reader.Read())
            {
                slsql = reader.GetInt32(0);
            }
            reader.Close();
            if (txtsl> slsql)
               
            {
                MessageBox.Show("Sach khong du chi con: " + slsql.ToString());
            }
            else
            {
                sqlCmd.CommandText = "INSERT INTO Bill VALUES ('" + txtBUYTheLoai.Text + "' , '" + txtBUYTenSach.Text+"' , '"+txtBUYSoLuong.Text+"', '"+ thanhtien.ToString()+"', '"+txtBUYNgay.Text+"')";
                SqlDataReader reader1 = sqlCmd.ExecuteReader();
                reader1.Close();
                hienthidanhsachbuy();
                soluongsaukhimua = slsql - txtsl;
                sqlCmd.CommandText = "UPDATE KhoSach SET soluong = "+soluongsaukhimua.ToString()+ " WHERE  tensach='" + txtBUYTenSach.Text + "'";
                SqlDataReader rd = sqlCmd.ExecuteReader();
                rd.Close();
                DTGRV1.Rows.Clear();
                hienthidanhsach();
            }    
                
           
        }

        private void btnCapnhat_Click(object sender, EventArgs e)
        {
            if (txtADDTenSach.Text != "" ||txtADDSoLuong.Text != "" || txtADDTacGia.Text != "" || txtADDNXB.Text != "" || txtADDLoaiSach.Text != "" || txtADDSoLuong.Text != "" || txtBUYGiaTien.Text != "" ) {
                
                sqlCon = new SqlConnection(strCon);
                sqlCon.Open();

                SqlCommand sqlCmd = new SqlCommand();
                sqlCmd.CommandType = CommandType.Text;
                sqlCmd.CommandText = "INSERT INTO KhoSach VALUES ('" + txtADDLoaiSach.Text + "' , '" + txtADDTenSach.Text + "', '" + txtADDTacGia.Text + "', '" + txtADDNXB.Text + "','" + txtADDSoLuong.Text + "','" + txtADDGiaTien.Text + "')";
                sqlCmd.Connection = sqlCon;
                SqlDataReader rd = sqlCmd.ExecuteReader();
                DTGRV1.Rows.Clear();
                hienthidanhsach();
                rd.Close();
            }
            else MessageBox.Show("Nhập Đủ Thông Tin!");

        }

        private void btnFind_Click(object sender, EventArgs e)
        {
            dataGridView1.Rows.Clear();
            sqlCon = new SqlConnection(strCon);
            sqlCon.Open();

            SqlCommand sqlCmd = new SqlCommand();
            sqlCmd.CommandType = CommandType.Text;
            if(ckbTheLoai.Checked)
                sqlCmd.CommandText = "select theloai,tensach,tacgia,nxb from KhoSach where theloai = '"+txtFINDTheLoai.Text+"'";
            if(chkTacGia.Checked)
                sqlCmd.CommandText = "select theloai,tensach,tacgia,nxb from KhoSach where tacgia = '" + txtFINDTacGia.Text + "'";
            if (chkNXB.Checked)
                sqlCmd.CommandText = "select theloai,tensach,tacgia,nxb from KhoSach where nxb = '" + txtFINDNXB.Text + "'";
            sqlCmd.Connection = sqlCon;
            SqlDataReader dataReader = sqlCmd.ExecuteReader();
            while (dataReader.Read())
            {
                DataGridViewRow dr = (DataGridViewRow)dataGridView1.Rows[0].Clone();

                dr.Cells[0].Value = dataReader.GetString(0);
                dr.Cells[1].Value = dataReader.GetString(1);
                dr.Cells[2].Value   = dataReader.GetString(2);
                dr.Cells[3].Value   = dataReader.GetString(3);

                dataGridView1.Rows.Add(dr);
            }
            dataReader.Close();
        }

        private void btnThongKe_Click(object sender, EventArgs e)
        {
            dataGridView2.Rows.Clear();
            sqlCon = new SqlConnection(strCon);
            sqlCon.Open();

            SqlCommand sqlCmd = new SqlCommand();
            sqlCmd.CommandType = CommandType.Text;
            if (chkVALUETheLoai.Checked)
                sqlCmd.CommandText = "select theloai,tensach,soluong,thanhtien,ngaymua from Bill where theloai = '" + txtVALUETheLoai.Text + "'";
            if (chkVALUENgay.Checked)
                sqlCmd.CommandText = "select theloai,tensach,soluong,thanhtien,ngaymua from Bill where ngaymua = '" + txtVALUENgay.Text + "'";
            sqlCmd.Connection = sqlCon;
            SqlDataReader reader = sqlCmd.ExecuteReader();
            
            while (reader.Read())
            {
                DataGridViewRow row = (DataGridViewRow)dataGridView2.Rows[0].Clone();
                row.Cells[0].Value = reader.GetString(0);
                row.Cells[1].Value = reader.GetString(1);
                row.Cells[2].Value = reader.GetInt32(2);
                row.Cells[3].Value = reader.GetInt32(3);
                DateTime dateValue = reader.GetDateTime(4);
                myDateVariable = dateValue;
                string ns = myDateVariable.ToString();
                string substr = ns.Substring(0, 10);
                row.Cells[4].Value = substr;
                dataGridView2.Rows.Add(row);    
            }
            reader.Close();
        }

        private void DTGRV2_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            int i = DTGRV2.CurrentRow.Index;
            txtBUYTheLoai.Text = DTGRV2.Rows[i].Cells[0].Value.ToString();
            txtBUYTenSach.Text = DTGRV2.Rows[i].Cells[1].Value.ToString();
            txtBUYSoLuong.Text = DTGRV2.Rows[i].Cells[2].Value.ToString();
            txtBUYGiaTien.Text = DTGRV2.Rows[i].Cells[3].Value.ToString();
            txtBUYNgay.Text = DTGRV2.Rows[i].Cells[4].Value.ToString();
        }

        private void btnEdit_Click(object sender, EventArgs e)
        {
            sqlCon = new SqlConnection(strCon);
            sqlCon.Open();
            SqlCommand sqlCmd = new SqlCommand();
            sqlCmd.CommandType = CommandType.Text;
            sqlCmd.Connection = sqlCon;
            sqlCmd.CommandText = "UPDATE KhoSach SET theloai='" + txtADDLoaiSach.Text + "', tacgia='" + txtADDTacGia.Text + "', nxb='" + txtADDNXB.Text + "', soluong = '" + txtADDSoLuong.Text + "',giatien='" + txtADDGiaTien.Text + "' WHERE tensach='" + txtADDTenSach.Text + "'";
            SqlDataReader rd = sqlCmd.ExecuteReader();
            rd.Close();
            DTGRV1.Rows.Clear();
            hienthidanhsach();
        }

        private void DTGRV1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            int i = DTGRV1.CurrentRow.Index;
            txtADDLoaiSach.Text = DTGRV1.Rows[i].Cells[0].Value.ToString();
            txtADDTenSach.Text = DTGRV1.Rows[i].Cells[1].Value.ToString();
            txtADDTacGia.Text = DTGRV1.Rows[i].Cells[2].Value.ToString();
            txtADDNXB.Text = DTGRV1.Rows[i].Cells[3].Value.ToString();
            txtADDSoLuong.Text = DTGRV1.Rows[i].Cells[4].Value.ToString();
            txtADDGiaTien.Text = DTGRV1.Rows[i].Cells[5].Value.ToString();

        }

        private void btnXoa_Click(object sender, EventArgs e)
        {
            sqlCon = new SqlConnection(strCon);
            sqlCon.Open();

            SqlCommand sqlCmd = new SqlCommand();
            sqlCmd.CommandType =CommandType.Text;
            sqlCmd.CommandText = "DELETE FROM KhoSach WHERE tensach='"+txtADDTenSach.Text+"'";
            sqlCmd.Connection = sqlCon;

            SqlDataReader reader = sqlCmd.ExecuteReader();
            reader.Close();
            DTGRV1.Rows.Clear();
            hienthidanhsach();
        }

        private void btnclose_Click(object sender, EventArgs e)
        {
            DialogResult dlr = MessageBox.Show("Bạn có muốn thoát không?", "Thoát?", MessageBoxButtons.YesNo,MessageBoxIcon.Question);
            
            if (dlr == DialogResult.Yes)
            {
                MessageBox.Show("Cảm ơn và hẹn gặp lại!");
                Close();
            }
            else if (dlr == DialogResult.No)
                MessageBox.Show("Đã hủy!");

        }

        private void ckbTheLoai_CheckedChanged(object sender, EventArgs e)
        {

            if (ckbTheLoai.Checked)
            {
                txtFINDTheLoai.Visible = true;
            }
            else
            {
                txtFINDTheLoai.Visible = false;
            }
        }

        private void tabPage3_Click(object sender, EventArgs e)
        {
           
        }

        private void txtFINDTheLoai_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void chkTacGia_CheckedChanged(object sender, EventArgs e)
        {
            if (chkTacGia.Checked)
            {
                txtFINDTacGia.Visible = true;
            }
            else
            {
                txtFINDTacGia.Visible = false;
            }
        }

        private void txtFINDTacGia_TextChanged(object sender, EventArgs e)
        {

        }

        private void chkNXB_CheckedChanged(object sender, EventArgs e)
        {
            if (chkNXB.Checked)
            {
                txtFINDNXB.Visible = true;
            }
            else
            {
                txtFINDNXB.Visible = false;
            }
        }

        private void txtFINDNXB_TextChanged(object sender, EventArgs e)
        {

        }

        private void chkVALUETheLoai_CheckedChanged(object sender, EventArgs e)
        {
            if (chkVALUETheLoai.Checked)
            {
                txtVALUETheLoai.Visible = true;
            }
            else
            {
                txtVALUETheLoai.Visible = false;
            }
        }

        private void txtVALUETheLoai_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void txtVALUENgay_ValueChanged(object sender, EventArgs e)
        {

           
        }

        private void chkVALUENgay_CheckedChanged(object sender, EventArgs e)
        {

            if (chkVALUENgay.Checked)
            {
                txtVALUENgay.Visible = true;
            }
            else
            {
                txtVALUENgay.Visible = false;
            }
        }
    }
}
