<?php
class CheckIp {

	public static $status;

	public function check($ip, $port) {
		$tcp = $this->checktcp($ip, $port);
		$icmp = $this->checkicmp($ip, $port);
		return json_encode(['ip' => $ip, 'port' => $port, 'tcp' => $tcp, 'icmp' => $icmp]);
	}
	// tcp
	public function checktcp($ip, $port) {
		$sock = @socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
		socket_set_nonblock($sock);
		socket_connect($sock, $ip, $port);
		socket_set_block($sock);
		$s1 = array($sock);
		$s2 = array($sock);
		$s3 = array($sock);
		self::$status = socket_select($s1, $s2, $s3, 5);
		if (self::$status == 2) {
			return 'fail';
		} else if (self::$status == 1) {
			return 'success';
		} else if (self::$status == 0) {
			return 'fail';
		}
		return null;
	}

	// icmp
	public function checkicmp($ip, $port) {

		$data = 'Z' . 'F' . chr(0) . chr(211);

		//ping程序凑够64byte的报文,这里包括IP首部20byte
		for ($i = 0; $i < 56; $i++) {
			$data .= chr(0);
		}

		$result = $this->sendPackage($ip, 8, 0, $data, function ($message) {});

		if ($result != null) {

			return $result;

		} else {
			return 'success';
		}
	}

	public function sendPackage($host, $type, $code, $data, $callbackfunc) {

		$g_icmp_error = null;

		$package = chr($type) . chr($code);

		$package .= chr(0) . chr(0);

		$package .= $data;

		$this->setSum($package);

		$socket = @socket_create(AF_INET, SOCK_RAW, getprotobyname('icmp'));

		if ($socket == false) {
			//在linux下socket icmp无法被创建 所以用exec来测试
			$i = @exec("ping $host -c 1");
			if (empty($i)) {
				return 'fail';
			}
			return 'success';

		}

		socket_sendto($socket, $package, strlen($package), 0, $host, 0);

		$read = array($socket);

		$write = NULL;

		$except = NULL;

		$select = socket_select($read, $write, $except, 0, 300 * 1000);

		if ($select === NULL) {

			$g_icmp_error = "Error";

			socket_fail($socket);

			return $g_icmp_error;

		} elseif ($select === 0) {

			$g_icmp_error = "TimeOut";

			socket_fail($socket);

			return $g_icmp_error;

		}
		socket_recvfrom($socket, $recv, 65535, 0, $host, $port);

		call_user_func($callbackfunc, $recv);

		return $g_icmp_error;
	}

	public function setSum(&$data) {

		$list = unpack('n*', $data);

		$length = strlen($data);

		$sum = array_sum($list);

		if ($length % 2) {

			$tmp = unpack('C*', $data[$length - 1]);
			$sum += $tmp[1];

		}

		$sum = ($sum >> 16) + ($sum & 0xffff);

		$sum += ($sum >> 16);

		$r = pack('n*', ~$sum);

		$data[2] = $r[0];

		$data[3] = $r[1];

	}

}

header('content-type:application/json');

header("Access-Control-Allow-Origin:*");

header('Access-Control-Allow-Methods:POST');

header('Access-Control-Allow-Headers:x-requested-with, content-type');

$ip = @$_POST['ip'];

$port = @$_POST['port'];

if (empty($ip) || empty($port)) {

	echo json_encode(['code' => 1, 'msg' => '缺少參數']);

} else {

	$health = new CheckIp();

	echo $health->check($ip, $port);

}
