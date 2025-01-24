using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement; // Thêm để quản lý scene

public class CarStoreManagerScript : MonoBehaviour
{
    public Transform content; // Đối tượng Content của Scroll View
    public GameObject carItemPrefab; // Prefab của từng Item

    public Sprite[] carImages; // Danh sách hình ảnh các xe
    public string[] carQuality;  // Danh sách tên các xe
    public int[] carPrices;    // Danh sách giá xe

    

    private void Start()
    {
        // Khởi tạo danh sách xe
        for (int i = 0; i < carQuality.Length; i++)
        {
            GameObject item = Instantiate(carItemPrefab, content); // Tạo bản sao của Prefab
            CarInfor carItem = item.GetComponent<CarInfor>(); // Lấy script CarInfor trên Prefab
            carItem.setCar(carImages[i], carQuality[i], carPrices[i]); // Gán thông tin cho từng xe
        }

        
    }

    
}
