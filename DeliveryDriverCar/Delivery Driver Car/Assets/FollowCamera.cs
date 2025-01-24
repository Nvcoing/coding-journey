using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FollowCamera : MonoBehaviour
{
    [SerializeField] GameObject thingToFollow; 

    void LateUpdate()
    {
       
        Vector3 newPosition = thingToFollow.transform.position + new Vector3(0, 0, -10);
        transform.position = newPosition;

       
        transform.rotation = Quaternion.identity;
    }
}
