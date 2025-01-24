using UnityEngine;
using UnityEngine.SceneManagement;
using TMPro;

public class PauseMenuController : MonoBehaviour
{
    [SerializeField] private GameObject pauseMenuUI;
    [SerializeField] private GameObject storeMenuUI; // Menu store khi nhấn B

    private bool isPaused = false;

    [SerializeField] private float countdownTime = 300f; // 5 phút = 300 giây
    private float timer;

    [SerializeField] private TextMeshProUGUI countdownText;
    [SerializeField] private TextMeshProUGUI coinText, coinText1; // Hiển thị số coin
    [SerializeField] private TextMeshProUGUI scoreText; // Hiển thị số coin
    public int currentCoins = 0; // Số coin hiện tại
    public int currentScore = 0; // Số coin hiện tại
    public int winConditionCoins = 1000; // Điều kiện thắng

    void Start()
    {
        timer = countdownTime; // Đặt thời gian bắt đầu là 5 phút
        UpdateCountdownText(); // Hiển thị giá trị ban đầu (5:00)
        UpdateCoinText(); // Hiển thị số coin ban đầu
    }

    void Update()
    {
        // Đếm ngược thời gian
        if (!isPaused)
        {
            timer -= Time.unscaledDeltaTime;
            if (timer <= 0)
            {
                timer = 0; // Đảm bảo không xuống dưới 0
                CheckGameEnd(); // Kiểm tra điều kiện kết thúc game
            }
            UpdateCountdownText();
        }

        // Bật/tắt menu tạm dừng
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            if (isPaused)
            {
                ResumeGame();
            }
            else
            {
                PauseGame();
            }
        }
        else if (Input.GetKeyDown(KeyCode.B)) // Mở menu store khi nhấn B
        {
            if (storeMenuUI.activeSelf) // Nếu menu store đang mở, đóng lại
            {
                ResumeGame();
            }
            else
            {
                OpenStoreMenu(); // Mở menu store
            }
        }
    }

    public void AddCoins(int amount,int score)
    {
        // Kiểm tra nếu trừ coin sẽ không làm coin âm
        if (currentCoins + amount >= 0)
        {
            currentCoins += amount;
            currentScore += score;
            UpdateCoinText();
            UpdateScoreText();
        }
        else
        {
            // Nếu số coin sẽ bị âm, set về 0
            currentCoins = 0;
            UpdateCoinText();
        }
    }

    private void CheckGameEnd()
    {
        if (currentScore >= winConditionCoins)
        {
            SceneManager.LoadScene("Win"); // Chuyển sang scene Win nếu đạt đủ coin
        }
        else
        {
            SceneManager.LoadScene("Lost"); // Chuyển sang scene Lost nếu không đủ coin
        }
    }

    private void UpdateCoinText()
    {
        coinText.text = "" + currentCoins;
        coinText1.text = "" + currentCoins;
    }
    private void UpdateScoreText()
    {
        scoreText.text = "" + currentScore;
    }
    // Ham thanh toan xe
    public bool SpeedCar(int price)
    {
        if (currentCoins >= price)
        {
            currentCoins -= price;
            Debug.Log("Mua xe thanh cong!");
            UpdateCoinText();
            return true;
        }
        else
        {
            Debug.Log("Khong du tien!");
            return false;
        }
    }

    public void ResumeGame()
    {
        pauseMenuUI.SetActive(false);
        storeMenuUI.SetActive(false); // Đảm bảo đóng menu store khi resume
        Time.timeScale = 1f;
        isPaused = false;
    }

    private void PauseGame()
    {
        pauseMenuUI.SetActive(true);
        Time.timeScale = 0f;
        isPaused = true;
    }

    private void OpenStoreMenu()
    {
        storeMenuUI.SetActive(true);
        Time.timeScale = 0f; // Dừng thời gian khi mở menu store
    }

    public void RestartGame()
    {
        Time.timeScale = 1f;
        SceneManager.LoadScene(SceneManager.GetActiveScene().name);
    }

    private void UpdateCountdownText()
    {
        int minutes = Mathf.FloorToInt(timer / 60);
        int seconds = Mathf.FloorToInt(timer % 60);
        countdownText.text = string.Format("{0:00}:{1:00}", minutes, seconds);
    }
}
