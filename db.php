<?php
function hs($text){
  $text = htmlspecialchars($text, ENT_QUOTES, 'UTF-8');
  return $text;
}
if(isset($argv)){
  $mine_name = hs($argv[1]);
  $uuid = hs($argv[2]);
  $server = hs($argv[3]);
  $reqserver = hs($argv[4]);
  $reqspace = hs($argv[5]);
  $status = hs($argv[6]);

  try {
    $db = new PDO ("mysql:dbname=<DATABASE_NAME>;host=<HOST_NAME>; charset=utf8", "<USER_NAME>", "<PASSWORD>");
  } catch (PDOException $e) {
    echo 'DB接続エラー' . $e->getMessage();
  }
  $sql="UPDATE mine_sktoken SET {$reqspace}=:argv WHERE id=1;";
  $stmt=$db->prepare($sql);
  $stmt->bindValue(":argv",False,PDO::PARAM_BOOL);
  $stmt->execute();

  //ログ追加
  $sql="INSERT into mine_log (name,uuid,server,reqsul,reqserver,reqsulstatus) VALUES (:name,:uuid,:server,:reqsul,:reqserver,:reqsulstatus)";
  $stmt=$db->prepare($sql);
  $stmt->bindValue(":name",$mine_name,PDO::PARAM_STR);
  $stmt->bindValue(":uuid",$uuid,PDO::PARAM_STR);
  $stmt->bindValue(":server",$server,PDO::PARAM_STR);
  $stmt->bindValue(":reqsul",true,PDO::PARAM_BOOL);
  $stmt->bindValue(":reqserver",$reqserver,PDO::PARAM_STR);
  if($status=="start"){
    $stmt->bindValue(":reqsulstatus","ok",PDO::PARAM_STR);
  }elseif($status=="cancel"){
    $stmt->bindValue(":reqsulstatus","cancel",PDO::PARAM_STR);
  }elseif($status=="nores"){
    $stmt->bindValue(":reqsulstatus","nores",PDO::PARAM_STR);
  }
  $stmt->execute();
}
