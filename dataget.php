<?php
define("PUSHOVER",FALSE);
define("EMAIL",FALSE);
$mailto = "cloud@v-count.com";

//$message = "<FieldSeparator>PublicIP=192.168.1.1<FieldSeparator>CustomerID=000001<FieldSeparator>DeviceID=000275<FieldSeparator>SendACK=2<FieldSeparator>IncomingHumanCount=10<FieldSeparator>MeasurementEndTime=2012-11-30 13:09:59<FieldSeparator>MeasurementStartTime=2012-11-30 13:00:00<FieldSeparator>OutgoingHumanCount=12<FieldSeparator>UUID=78a77496-c969-4adc-9be2-80b0759b578c<FieldSeparator>\r\n";
$message = "<FieldSeparator>CustomerID=000001<FieldSeparator>DeviceID=000275<FieldSeparator>SendACK=0<FieldSeparator>IncomingHumanCount=10<FieldSeparator>MeasurementEndTime=2012-11-30 13:09:59<FieldSeparator>MeasurementStartTime=2012-11-30 13:00:00<FieldSeparator>OutgoingHumanCount=12<FieldSeparator>PublicIP=NONE<FieldSeparator>UUID=78a77496-c969-4adc-9be2-80b0759b578c\n";

$html = date("d.m.Y H:i:s")."<br /><br />";

$ip = '54.154.163.83';
$port = '12100';

$errorcode = "";
$errormsg = "";

if(!($sock = socket_create(AF_INET, SOCK_STREAM, 0)))
{
    $errorcode = socket_last_error();
    $errormsg = socket_strerror($errorcode);
    
    $html .= $errormsg;
    
    send_mail($mailto, "Couldn't create socket: [$errorcode]", $html);
    pushover("Couldn't create socket: [$errorcode]");
    die();
}
 
echo "Socket created\n";

if(!socket_connect($sock , $ip , $port))
{
    $errorcode = socket_last_error();
    $errormsg = socket_strerror($errorcode);
     
    $html .= $errormsg;
    
    send_mail($mailto, "Could not connect: [$errorcode]", $html);
    pushover("Could not connect: [$errorcode]");
    die();
}
 
echo "Connection established \n";

//Send the message to the server
$x = 0;
while($x < 5 && strlen($message) <  socket_send ( $sock , $message , strlen($message) , 0)){
    $x++;
    echo "Not successful, trying again.";
    if($x==5)
    {
        $errorcode = socket_last_error();
        $errormsg = socket_strerror($errorcode);

        $html .= $errormsg;

        send_mail($mailto, "Could not send all data after having tried ".$x." times: [$errorcode]", $html);
        pushover("Could not send all data after having tried ".$x." times: [$errorcode]");
        die();
    }
}
 
echo "Message sent successfully \n";

//Now receive reply from server
$recv = socket_recv ( $sock , $buf , 5000 , MSG_WAITALL );
if($recv === FALSE)
{
    $errorcode = socket_last_error();
    $errormsg = socket_strerror($errorcode);
    
    $html .= $errormsg;
    
    send_mail($mailto, "Could not receive data: [$errorcode]", $html);
    pushover("Could not receive data: [$errorcode]");
    die();
}
 
$html .= "recv: ".$recv."<br /><br />";
$html .= "buf: ".$buf."<br /><br />";
$html .= $errormsg;

//echo "html: ".$html."\n";

if($buf != "78a77496-c969-4adc-9be2-80b0759b578c") {
    send_mail($mailto, "Received data is wrong: [$errorcode]", $html);
    pushover("Received data is wrong: [$errorcode]");
    die();
}

//print the received message
echo "buf: ".$buf;
//echo "Hurray!";

socket_close($sock);

//$ip_address = gethostbyname("www.google.com");

function pushover($message) {
    
    if(PUSHOVER) {
        $post_array = array(
                'token' => "abAQiLvWryFJ8QYX159V2oHCnTfjax",
                'user' => "gF7zPhY6AorUKRouCasNL5TcVcobBY",
                'message' => $message,
                'priority' => "1",
                'retry' => "60",
                'expire' => "3600"
        );

        $url = "https://api.pushover.net/1/messages.json";

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, true);

        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_array);
        $output = curl_exec($ch);
        $info = curl_getinfo($ch);

        $curlerrcode = curl_errno($ch);
        $curlerr = curl_error($ch);

        curl_close($ch);
    }
}

function send_mail($to, $subject, $html) {
    
    $headers = "MIME-Version: 1.0" . "\r\n";
    $headers .= "Content-type:text/html;charset=utf-8" . "\r\n";;
    $headers .= "From: V-Count <noreply@v-count.com> \n";
    $headers .= "Reply-To: noreply@v-count.com \n";

    if(EMAIL) {
        mail($to, $subject, $html, $headers, "-f noreply@v-count.com");
    }
}

?>
