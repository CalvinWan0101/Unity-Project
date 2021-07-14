using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MicroPhoneInput : MonoBehaviour
{
    private string microphoneName;
    private AudioSource audioSource;
    void Start()
    {
        audioSource = GetComponent<AudioSource>();
        foreach (var device in Microphone.devices)
        {
            if (microphoneName == null)
            {
                microphoneName = device;
            }
        }
        UpdateMicrophone();
    }
    void UpdateMicrophone()
    {
        audioSource.Stop();
        //Start recording to audioclip from the mic
        audioSource.clip = Microphone.Start(microphoneName, true, 10, 44100);
        audioSource.loop = true;
        // Mute the sound with an Audio Mixer group becuase we don't want the player to hear it
        Debug.Log(Microphone.IsRecording(microphoneName).ToString());

        if (Microphone.IsRecording(microphoneName))
        { //check that the mic is recording, otherwise you'll get stuck in an infinite loop waiting for it to start
            while (!(Microphone.GetPosition(microphoneName) > 0))
            {
            } // Wait until the recording has started. 

            Debug.Log("recording started with " + microphoneName);

            // Start playing the audio source
            audioSource.Play();
        }
        else
        {
            //microphone doesn't work for some reason

            Debug.Log(microphoneName + " doesn't work!");
        }
    }
    private void Update()
    {
    }
}
