using UnityEngine;
using System.Collections.Generic;

public class PolicePatrolController : MonoBehaviour
{
    public AudioSource musicAudioSfx;
    public AudioClip musicSiren;
    [Header("Movement Settings")]
    [SerializeField] private float patrolSpeed = 8f;
    [SerializeField] private float chaseSpeed = 12f;
    [SerializeField] private float rotateSpeed = 180f;

    [Header("Detection Settings")]
    [SerializeField] private float detectionRange = 15f;
    [SerializeField] private float targetPointRadius = 0.5f;

    private Rigidbody2D rb;
    private Transform playerTarget;
    private Vector2 currentTargetPoint;
    private bool isChasing;
    private bool hasTarget;
    private List<Vector2> visitedPoints = new List<Vector2>();
    private GameObject[] roadObjects;
    private int maxVisitedPoints = 10;

    private void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        playerTarget = GameObject.FindGameObjectWithTag("Player")?.transform;
        roadObjects = GameObject.FindGameObjectsWithTag("Road");
        FindNewTargetPoint();
        musicAudioSfx.clip = musicSiren;
        musicAudioSfx.loop = true;
    }

    private void FixedUpdate()
    {
        if (playerTarget == null) return;

        CheckPlayerDetection();

        if (isChasing)
        {
            if (!musicAudioSfx.isPlaying)
            {
                musicAudioSfx.Play();
            }
            ChasePlayer();
        }
        else
        {
            musicAudioSfx.Stop();
            PatrolRoads();
        }
    }

    private void FindNewTargetPoint()
    {
        if (roadObjects.Length == 0) return;

        float minDistance = float.MaxValue;
        Vector2 bestPoint = rb.position;
        bool foundValidPoint = false;

        // Tìm object Road gần nhất chưa được thăm
        foreach (GameObject road in roadObjects)
        {
            if (road == null) continue;

            // Lấy bounds của road object
            Renderer roadRenderer = road.GetComponent<Renderer>();
            if (roadRenderer == null) continue;

            // Tạo một số điểm ngẫu nhiên trong bounds của road
            for (int i = 0; i < 5; i++)
            {
                Vector2 randomPoint = GetRandomPointOnRoad(roadRenderer.bounds);

                // Kiểm tra xem điểm này có quá gần điểm đã thăm không
                bool isTooClose = false;
                foreach (Vector2 visitedPoint in visitedPoints)
                {
                    if (Vector2.Distance(randomPoint, visitedPoint) < 2f)
                    {
                        isTooClose = true;
                        break;
                    }
                }

                if (!isTooClose)
                {
                    float distance = Vector2.Distance(rb.position, randomPoint);
                    if (distance < minDistance)
                    {
                        minDistance = distance;
                        bestPoint = randomPoint;
                        foundValidPoint = true;
                    }
                }
            }
        }

        if (foundValidPoint)
        {
            currentTargetPoint = bestPoint;
            hasTarget = true;

            // Thêm điểm vào danh sách đã thăm
            visitedPoints.Add(currentTargetPoint);
            if (visitedPoints.Count > maxVisitedPoints)
            {
                visitedPoints.RemoveAt(0);
            }
        }
        else
        {
            // Nếu không tìm được điểm mới, xóa lịch sử để bắt đầu lại
            visitedPoints.Clear();
            FindNewTargetPoint();
        }
    }

    private Vector2 GetRandomPointOnRoad(Bounds bounds)
    {
        return new Vector2(
            Random.Range(bounds.min.x, bounds.max.x),
            Random.Range(bounds.min.y, bounds.max.y)
        );
    }

    private void PatrolRoads()
    {
        if (!hasTarget || Vector2.Distance(rb.position, currentTargetPoint) < targetPointRadius)
        {
            FindNewTargetPoint();
        }

        if (hasTarget)
        {
            MoveToTarget(currentTargetPoint);
        }
    }

    private void CheckPlayerDetection()
    {
        float distanceToPlayer = Vector2.Distance(rb.position, playerTarget.position);
        isChasing = distanceToPlayer <= detectionRange;
    }

    private void ChasePlayer()
    {
        if (playerTarget == null) return;
        MoveToTarget(playerTarget.position);
    }

    private void MoveToTarget(Vector2 target)
    {
        // Tính hướng di chuyển
        Vector2 direction = (target - rb.position).normalized;

        // Tính góc cần xoay
        float targetAngle = Mathf.Atan2(direction.y, direction.x) * Mathf.Rad2Deg - 90f;
        float angleDifference = Mathf.DeltaAngle(transform.eulerAngles.z, targetAngle);
        float rotationAmount = Mathf.Clamp(angleDifference, -rotateSpeed * Time.fixedDeltaTime, rotateSpeed * Time.fixedDeltaTime);

        // Áp dụng xoay
        transform.rotation = Quaternion.Euler(0, 0, transform.eulerAngles.z + rotationAmount);

        // Di chuyển
        float currentSpeed = isChasing ? chaseSpeed : patrolSpeed;
        Vector2 movement = (Vector2)transform.up * currentSpeed * Time.fixedDeltaTime;
        rb.MovePosition(rb.position + movement);
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        // Tìm điểm mới khi va chạm
        hasTarget = false;
    }

    private void OnDrawGizmos()
    {
        // Vẽ vùng phát hiện player
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(transform.position, detectionRange);

        // Vẽ điểm đích hiện tại
        if (hasTarget)
        {
            Gizmos.color = Color.red;
            Gizmos.DrawWireSphere(currentTargetPoint, targetPointRadius);
        }

        // Vẽ các điểm đã thăm
        Gizmos.color = Color.blue;
        foreach (Vector2 point in visitedPoints)
        {
            Gizmos.DrawWireSphere(point, 0.3f);
        }
    }
}