using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NewBehaviourScript : MonoBehaviour
{
    // Start is called before the first frame update
    public float velocidadMovimiento = 5.0f;
    public float velocidadRotacion = 200.0f;
    private Animator anim;
    public UDPReceive udpReceive;
    public float x, y;
    public float a, b;

    void Start()
    {
        anim = GetComponent<Animator>();
    }

    // Update is called once per frame
    void Update()
    {
        string data = udpReceive.data;
        data = data.Remove(0, 1);
        data = data.Remove(data.Length - 1, 1);
        print(data);
        string[] points = data.Split(',');
        a = float.Parse(points[0]) - float.Parse(points[1]);
        if (a > 0){
            x = 1;
        } 
        else if (a == 0)
        {
            x = 0;
        }
        else 
        {
            x = -1;
        }

        b = float.Parse(points[2]) - float.Parse(points[3]);
        if ( b > 0){
            y = 1;
        } 
        else if (b == 0)
        {
            y = 0;
        }
        else
        { 
            y = -1; 
        }
        
        

        transform.Rotate(0, x * Time.deltaTime * velocidadRotacion, 0);
        transform.Translate(0, 0, y * Time.deltaTime * velocidadMovimiento);

        anim.SetFloat("VelX", x);
        anim.SetFloat("VelY", y);
    }
}
