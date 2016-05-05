<?php

// base class with member properties and methods
class trackeddevice {
	var $id;
	var $name;
	var $locationx;
	var $locationy;
	var $locationz;
	var $lastseentime;
	
	function trackeddevice($id, $name,$locationx, $locationy, $locationz, $lastseentime) 
	{
		$this->id = $id;
		$this->name = $name;
		$this->locationx = $locationx;
		$this->locationy = $locationy;
		$this->locationz = $locationz;
		$this->lastseentime = $lastseentime;
	}

	function get_id() 
	{
		return $this->id;
	}

	function set_id($id) 
	{
		$this->id = $id;
	}

	function get_name() 
	{
		return $this->name;
	}

	function set_name($name) 
	{
		$this->name = $name;
	}

	function get_locationx() 
	{
		return $this->locationx;
	}

	function set_locationx($locationx) 
	{
		$this->locationx = $locationx;
	}

	function get_locationy() 
	{
		return $this->locationy;
	}

	function set_locationy($locationy) 
	{
		$this->locationy = $locationy;
	}

	function get_locationz() 
	{
		return $this->locationz;
	}

	function set_locationz($locationz) 
	{
		$this->locationz = $locationz;
	}

	function get_lastseentime() 
	{
		return $this->lastseentime;
	}

	function set_lastseentime($lastseentime) 
	{
		$this->lastseentime = $lastseentime;
	}

} // end of class trackeddevice
?>
