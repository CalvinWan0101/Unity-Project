using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Cube_move : MonoBehaviour
{
    //speed can be change
    public int speed;
    public float rotate_speed;
    float final_speed=0.01f;
    // Start is called before the first frame update
    void Start()
    {
        final_speed *= speed;
        Debug.Log(final_speed);
    }

    // Update is called once per frame
    void Update()
    {
        //R = red
        if (Input.GetKeyDown(KeyCode.R))
            GetComponent<Renderer>().material.color = Color.red;
        //G = green
        if (Input.GetKeyDown(KeyCode.G))
            GetComponent<Renderer>().material.color = Color.green;
        //B = blue
        if (Input.GetKeyDown(KeyCode.B))
            GetComponent<Renderer>().material.color = Color.blue;
        //Y = yellow
        if (Input.GetKeyDown(KeyCode.Y))
            GetComponent<Renderer>().material.color = Color.yellow;


        //if(press A) x+= final_speed
        if (Input.GetKey(KeyCode.A)) 
            transform.Translate(final_speed , 0, 0); 
        //if(press D) x-= final_speed
        if (Input.GetKey(KeyCode.D)) 
            transform.Translate(-final_speed, 0, 0); 
        //if(press W) y+= final_speed
        if (Input.GetKey(KeyCode.W))
            transform.Translate(0, final_speed, 0); 
        //if(press S) y-= final_speed
        if (Input.GetKey(KeyCode.S))
            transform.Translate(0, -final_speed, 0);

        //press Q to back to (0,0,0)
        if (Input.GetKey(KeyCode.Q))
            transform.position = new Vector3(0, 0, 0);

        //if(press up) z+= final_speed
        if (Input.GetKey("up"))
            transform.Translate(0, 0, final_speed);
        //if(press down) z-= final_speed
        if (Input.GetKey("down"))
            transform.Translate(0, 0, -final_speed);
        //angle -= rotate_speed
        if (Input.GetKey("left"))
            transform.Rotate(rotate_speed, 0,0);
        //angle += rotate_speed
        if (Input.GetKey("right"))
            transform.Rotate(0, rotate_speed, 0);
    }
}