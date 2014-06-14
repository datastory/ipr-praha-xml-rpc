<?php

include 'xmlrpc.inc';
$sessionId = '';

// Vložení parametru, v tomto případě účelového. Uložený dotaz má v sobě účelovou podmínku "WHERE 1 = parametr1", tzn. výsledná podmínka je v tomto případě "WHERE 1 = 1".
$in_xml = '<?xml version="1.0" encoding="UTF-8"?>
<request>
	<params>
		<param>
			<parid>1</parid>
			<partype>NUMERIC</partype>
			<content>1</content>
		</param>
	</params>
</request>';


$server = new xmlrpc_client('/ws/RPC2/','app.urm.cz', 80);
$server->request_charset_encoding = 'UTF-8';

// $user='anonymous@ipr.praha.eu';
// $pasword_hash='294de3557d9d00b3d2d8a1e6aab028cf';

$user='hackathon';
$pasword_hash='c1d43a1b8cfa81c6b26fa036e328af0b';

//autentizace
$login_msg = new xmlrpcmsg('authenticate',
                         array(new xmlrpcval($user, 'string'),
                               new xmlrpcval($pasword_hash, 'string')));
							   
$login = $server->send($login_msg);

// Process the response.
if (!$login) {
    print "<p>Could not connect to HTTP server.</p>";
} elseif ($login->faultCode()) {
    print "<p>XML-RPC Fault #" . $login->faultCode() . ": " .
        $login->faultString();
} else {
    $sessionId = $login->value()->scalarVal();
}	

if(strlen($sessionId) > 0){	

	// $query_id = 381;
	$query_id = 502;
	$rows = 500;
	$offset = 0;
						 
	$query_msg =  new xmlrpcmsg('getstoredqueryresult',
                         array(new xmlrpcval($sessionId, 'string'),
								new xmlrpcval($query_id, 'int'),
								new xmlrpcval($rows, 'int'),
								new xmlrpcval($offset, 'int'),
								new xmlrpcval($in_xml, 'string')
						 ));
	
	//poslani dotazu
	$result = $server->send($query_msg);
	
if (!$result) {
    print "<p>XML-RPC Error</p>";
} elseif ($result->faultCode()) {
    print "<p>XML-RPC Fault #" . $result->faultCode() . ": " .
        $result->faultString();
} else {
    $obj = $result->value()->scalarVal();
}	

	print ($obj);

}

?>