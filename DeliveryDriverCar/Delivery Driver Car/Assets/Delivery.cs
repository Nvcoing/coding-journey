using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Delivery : MonoBehaviour
{
    [SerializeField] Color32 hasPackageColor = new Color32(1, 1, 1, 1);
    [SerializeField] Color32 noPackageColor = new Color32(0, 0, 0, 1);
    [SerializeField] float destroyDelay = 0.5f;

    SpriteRenderer spriteRenderer;

    private bool gotPackage = false;

    private Transform currentPackage;
    private Transform currentCustomer;

    private PauseMenuController pauseMenuController; // Tham chiếu đến PauseMenuController

    void Start()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
        pauseMenuController = FindObjectOfType<PauseMenuController>(); // Tìm PauseMenuController trong scene
        FindNextPackage();
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.tag == "Package" && !gotPackage)
        {
            Debug.Log("Package Picked up!");
            gotPackage = true;
            spriteRenderer.color = hasPackageColor;
            currentPackage = other.transform;
            Destroy(other.gameObject, destroyDelay);
            FindNextCustomer();
        }
        else if (gotPackage && other.tag == "Customer")
        {
            Debug.Log("Package Delivered!");
            gotPackage = false;
            spriteRenderer.color = noPackageColor;

            if (pauseMenuController != null)
            {
                // Sử dụng hệ số điểm từ CarInfor
                pauseMenuController.AddCoins(50, 10 * CarInfor.currentScoreMultiplier);
            }

            currentCustomer = null;
            FindNextPackage();
        }
    }

    void FindNextPackage()
    {
        GameObject nextPackage = GameObject.FindWithTag("Package");

        if (nextPackage != null)
        {
            currentPackage = nextPackage.transform;
            Pointer pointer = FindObjectOfType<Pointer>();

            if (pointer != null)
            {
                pointer.SetTarget(currentPackage);
            }
            else
            {
                Debug.LogWarning("Pointer not found in the scene!");
            }
        }
        else
        {
            Debug.Log("No more packages left!");
            Pointer pointer = FindObjectOfType<Pointer>();
            if (pointer != null)
            {
                pointer.SetTarget(null);
            }
        }
    }

    void FindNextCustomer()
    {
        GameObject nextCustomer = GameObject.FindWithTag("Customer");

        if (nextCustomer != null)
        {
            currentCustomer = nextCustomer.transform;
            Pointer pointer = FindObjectOfType<Pointer>();

            if (pointer != null)
            {
                pointer.SetTarget(currentCustomer);
            }
            else
            {
                Debug.LogWarning("Pointer not found in the scene!");
            }
        }
        else
        {
            Debug.LogWarning("No more customers left!");
            Pointer pointer = FindObjectOfType<Pointer>();
            if (pointer != null)
            {
                pointer.SetTarget(null);
            }
        }
    }
}
