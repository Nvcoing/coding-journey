using UnityEngine;

public class AudioManagerScript : MonoBehaviour
{

    public static AudioManagerScript instance;
    // Bien lua tru cac Audio
    public AudioSource musicAudioSrc;
    public AudioSource musicAudioSfx;
    //Audio Clip


    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
            // Khong huy khi chuyen Scene
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }
    public void playMusic(AudioClip clip)
    {
        musicAudioSrc.clip = clip;
        musicAudioSrc.loop = true;
        musicAudioSrc.Play();
    }

    public void playSfx(AudioClip clip)
    {
        musicAudioSfx.clip = clip;
        musicAudioSfx.PlayOneShot(clip);
    }
}
