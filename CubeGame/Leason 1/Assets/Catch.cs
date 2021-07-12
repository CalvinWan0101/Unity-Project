using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Catch : MonoBehaviour
{
    // Start is called before the first frame update
    public GameObject target;
    void Start()
    {
        target = GameObject.Find("Cube");
    }
    void Update()
    {
        if (Input.GetKeyDown("space"))
            if(!target.activeInHierarchy)
                target.SetActive(true);
            else
                target.SetActive(false);
    }
}