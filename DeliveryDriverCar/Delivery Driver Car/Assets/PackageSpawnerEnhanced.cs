using System.Collections.Generic;
using UnityEngine;

public class SimplePackageSpawner : MonoBehaviour
{
    [SerializeField] private GameObject packagePrefab; // Prefab Package
    [SerializeField] private Transform roadsParent;    // Object Roads chứa các roads
    [SerializeField] private Transform packageList;    // Object chứa các package
    [SerializeField] private float spawnInterval = 5f; // Thời gian giữa mỗi lần spawn
    [SerializeField] private int maxPackages = 3;      // Số lượng package tối đa

    private float timer;
    private List<GameObject> activePackages = new List<GameObject>(); // Danh sách quản lý packages

    void Start()
    {
        timer = spawnInterval;
    }

    void Update()
    {
        // Đếm ngược thời gian
        timer -= Time.deltaTime;

        // Kiểm tra và loại bỏ các package đã bị hủy
        activePackages.RemoveAll(package => package == null);

        // Kiểm tra thời gian và số lượng package hiện tại
        if (timer <= 0 && activePackages.Count < maxPackages)
        {
            SpawnRandomPackage();
            timer = spawnInterval; // Reset timer
        }
    }

    void SpawnRandomPackage()
    {
        if (roadsParent != null && roadsParent.childCount > 0)
        {
            // Chọn ngẫu nhiên một road
            int randomRoadIndex = Random.Range(0, roadsParent.childCount);
            Transform selectedRoad = roadsParent.GetChild(randomRoadIndex);

            // Lấy kích thước của road được chọn
            Renderer roadRenderer = selectedRoad.GetComponent<Renderer>();
            if (roadRenderer != null)
            {
                // Tính toán vị trí ngẫu nhiên trong phạm vi của road
                Vector3 roadBounds = roadRenderer.bounds.size;
                Vector3 roadPosition = selectedRoad.position;

                float randomX = Random.Range(
                    roadPosition.x - roadBounds.x / 2,
                    roadPosition.x + roadBounds.x / 2
                );
                float randomZ = Random.Range(
                    roadPosition.z - roadBounds.z / 2,
                    roadPosition.z + roadBounds.z / 2
                );

                // Tạo package mới
                Vector3 spawnPosition = new Vector3(randomX, roadPosition.y, randomZ);
                GameObject newPackage = Instantiate(packagePrefab, spawnPosition, Quaternion.identity);

                // Gắn tag "Package" cho package mới
                newPackage.tag = "Package";

                // Đặt package làm con của PackageList
                if (packageList != null)
                {
                    newPackage.transform.parent = packageList;
                }

                // Thêm package vào danh sách quản lý
                activePackages.Add(newPackage);
            }
        }
    }
}
