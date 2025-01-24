using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;

public class MenuController : MonoBehaviour
{
    private bool isButtonClicked = false;
    //Audio Clip
    public AudioClip musicBtnStart;
    public AudioClip musicBackground;
    void Start()
    {
        AudioManagerScript.instance.playMusic(musicBackground);
    }

    public void StartGame()
    {
        if (isButtonClicked) return;
        isButtonClicked = true;

        Debug.Log("Start Game Button Pressed");

        AudioManagerScript.instance.playSfx(musicBtnStart);
        //Delay 0.5s de vao Scene
        StartCoroutine(LoadGameSceneAfterDelay(0.5f, "GamePlay"));
    }


    public void QuitGame()
    {
        if (isButtonClicked) return;
        isButtonClicked = true;

        Debug.Log("Quit Game Button Pressed");
        Application.Quit();
    }
    public void Menu()
    {
        AudioManagerScript.instance.playSfx(musicBtnStart);
        //Delay 0.5s de vao Scene
        StartCoroutine(LoadGameSceneAfterDelay(0.5f, "Menu"));
    }
    //void Update()
    //{

    //    if (Input.GetKeyDown(KeyCode.Escape))
    //    {

    //        SceneManager.LoadScene("Menu");  
    //    }
    //}
    public void RestartGame()
    {
        AudioManagerScript.instance.playSfx(musicBtnStart);
        //Delay 0.5s de vao Scene
        StartCoroutine(LoadGameSceneAfterDelay(0.5f, "GamePlay"));
        SceneManager.LoadScene("GamePlay");
    }
    // Ham delay va goi den Scene
    private IEnumerator LoadGameSceneAfterDelay(float delay, string s)
    {
        yield return new WaitForSeconds(delay);
        SceneManager.LoadScene(s);
    }
}
