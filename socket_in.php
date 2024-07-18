<?php
if(!empty($argv)){
  $mine_name = $argv[1];
  $uuid = $argv[2];
  $server = $argv[3];
  $reqserver = $argv[4];
  $reqspace = $argv[5];
  $status = $argv[6];
  // サーバーのIPアドレスとポート番号
  $serverAddress = '127.0.0.1';
  $serverPort = 8766;

  // ソケットを作成して接続
  $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
  socket_connect($socket, $serverAddress, $serverPort);

  if($status=="start"){
    $message = "PHP->req->start->管理者がリクエストを受諾しました。{$reqserver}サーバーがまもなく起動します。\n";
  }elseif($status=="cancel"){
    $message = "PHP->req->cancel->管理者がリクエストを拒否しました。\n";
  }elseif($status=="nores"){
    $message = "PHP->req->nores->管理者が応答しませんでした。\n";
  }
  // メッセージを送信
  socket_write($socket, $message, strlen($message));
  // ソケットを閉じる
  socket_close($socket);
}
