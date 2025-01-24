using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Pointer : MonoBehaviour
{
    [SerializeField] private Transform target;       // Mục tiêu mà mũi tên chỉ đến
    [SerializeField] private Transform player;       // Xe hoặc đối tượng trung tâm
    [SerializeField] private float distanceFromPlayer = 2f; // Khoảng cách từ mũi tên đến xe

    private float currentAngle = 0f; // Góc hiện tại của mũi tên quanh xe

    void Update()
    {
        if (target != null && player != null)
        {
            // Tính góc giữa player và target
            Vector2 direction = target.position - player.position;
            float angleToTarget = Mathf.Atan2(direction.y, direction.x) * Mathf.Rad2Deg;

            // Cập nhật góc quay
            currentAngle = Mathf.LerpAngle(currentAngle, angleToTarget, Time.deltaTime * 5f);

            // Tính vị trí mới của mũi tên dựa trên góc và khoảng cách
            float radianAngle = currentAngle * Mathf.Deg2Rad;
            Vector3 offset = new Vector3(Mathf.Cos(radianAngle), Mathf.Sin(radianAngle), 0) * distanceFromPlayer;
            transform.position = player.position + offset;

            // Quay mũi tên để chỉ về target
            transform.rotation = Quaternion.Euler(0, 0, currentAngle - 90);
        }
        else
        {
            gameObject.SetActive(false);
        }
    }

    public void SetTarget(Transform newTarget)
    {
        target = newTarget;

        if (target != null)
        {
            gameObject.SetActive(true);
        }
        else
        {
            gameObject.SetActive(false);
        }
    }
}
