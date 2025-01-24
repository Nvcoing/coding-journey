using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class CarInfor : MonoBehaviour
{
    public Image carImage;
    public TMP_Text qualityCar;
    public TMP_Text carPrice;
    public Button btnBuy;
    private int price;
    private Sprite carSprite;
    private Driver playerDriver;
    public static int currentScoreMultiplier = 1; // Thêm biến static để lưu hệ số điểm

    public static PauseMenuController player;

    void Start()
    {
        if (player == null)
        {
            player = FindObjectOfType<PauseMenuController>();
        }
        playerDriver = FindObjectOfType<Driver>();
    }

    public void setCar(Sprite image, string quality, int price)
    {
        carImage.sprite = image;
        carSprite = image;
        qualityCar.text = quality;
        this.price = price;
        carPrice.text = this.price.ToString();
    }

    public void OnBtnBuyClicked()
    {
        if (player.SpeedCar(price))
        {
            btnBuy.interactable = false;
            carPrice.text = "Purchased!";

            if (playerDriver != null)
            {
                SpriteRenderer playerSprite = playerDriver.GetComponent<SpriteRenderer>();
                if (playerSprite != null)
                {
                    playerSprite.sprite = carSprite;
                    // Set hệ số điểm dựa vào giá xe
                    if (price <= 100) currentScoreMultiplier = 5;
                    else if (price <= 300) currentScoreMultiplier = 10;
                    else currentScoreMultiplier = 50;
                }
            }
        }
    }
}