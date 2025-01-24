using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Driver : MonoBehaviour
{
    [SerializeField] float steerSpeed = 300f;
    [SerializeField] float moveSpeed = 20f;
    [SerializeField] float slowSpeed = 15f;
    [SerializeField] float boostSpeed = 30f;
    private SpriteRenderer spriteRenderer;

    private float normalSpeed;
    private Coroutine speedResetCoroutine;
    private PauseMenuController pauseMenuController;

    void Start()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
        if (spriteRenderer == null)
        {
            Debug.LogError("SpriteRenderer không tìm thấy trên object xe!");
        }
        normalSpeed = moveSpeed;

        pauseMenuController = FindObjectOfType<PauseMenuController>();
        if (pauseMenuController == null)
        {
            Debug.LogError("PauseMenuController không tìm thấy trong scene!");
        }
    }

    void Update()
    {
        float moveAmount = Input.GetAxis("Vertical") * moveSpeed * Time.deltaTime;

        // Chỉ cho phép rẽ khi xe đang di chuyển
        float steerAmount = 0f;
        if (Mathf.Abs(moveAmount) > 0.01f)  // Kiểm tra xe có đang di chuyển không
        {
            steerAmount = Input.GetAxis("Horizontal") * steerSpeed * Time.deltaTime;
            // Đảo hướng rẽ khi lùi
            if (moveAmount < 0)
            {
                steerAmount = -steerAmount;
            }
        }

        transform.Rotate(0, 0, -steerAmount);
        transform.Translate(0, moveAmount, 0);
    }

    void OnCollisionEnter2D(Collision2D other)
    {
        Debug.Log("Lowering the Speed");
        moveSpeed = slowSpeed;

        // Kiểm tra va chạm với cảnh sát
        if (other.gameObject.GetComponent<PolicePatrolController>() != null)
        {
            if (pauseMenuController != null && pauseMenuController.currentCoins > 0)
            {
                // Trừ 1 coin khi va chạm với cảnh sát
                pauseMenuController.AddCoins(-1, 0);
                Debug.Log("Bị trừ 1 coin do va chạm với cảnh sát!");
            }
        }

        if (speedResetCoroutine != null)
        {
            StopCoroutine(speedResetCoroutine);
        }
        speedResetCoroutine = StartCoroutine(ResetSpeedAfterDelay());
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.tag == "Speed Up")
        {
            Debug.Log("BOOST! Speed up incoming!");
            moveSpeed = boostSpeed;

            if (speedResetCoroutine != null)
            {
                StopCoroutine(speedResetCoroutine);
            }
        }
    }

    IEnumerator ResetSpeedAfterDelay()
    {
        yield return new WaitForSeconds(5f);
        moveSpeed = normalSpeed;
        Debug.Log("Speed restored to normal");
    }
}