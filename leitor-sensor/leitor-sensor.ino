//Trabalho de graduação - WebSensor - Gabriel Dornelas

// --- WIFI ---
// biblioteca para uso do wi-fi
#include <ESP8266WiFi.h>
// troque pelo nome da sua rede
const char* ssid = "Dornelas";
// troque pela senha da sua rede
const char* password = "ArEIAmOlhAdA39562652";
// objeto para conexão do wi-fi
WiFiClient nodemcuClient;

// --- MQTT ---
// biblioteca para uso do servidor MQTT
#include <PubSubClient.h>
// endereço do servidor
const char* mqtt_Broker = "iot.eclipse.org";
// nome do cliente para acessar o servidor
const char* mqtt_ClientID = "Gabriel";
// criando o servidor
PubSubClient client(nodemcuClient);
// nomeando tópico de temperatura do servidor
const char* topicoTemperatura = "sensorDornelas/temperatura";
// nomeando tópico de umidade do servidor
const char* topicoUmidade = "sensorDornelas/umidade";

// --- DHT ---
// biblioteca para uso do sensor de temperatura/umidade
#include <DHT.h>
// definição do pino a ser utilizado na placa nodemcu
#define DHTPIN D3
// definição do modelo do sensor a ser utilizado
#define DHTTYPE DHT11
// função para utilizar o sensor
DHT dht(DHTPIN, DHTTYPE);
// variável onde será armazenado dado de umidade
int umidade;
// variável onde será armazenado dado de temperatura
int temperatura;

// --- BOOT ---
// inicia o sistema
void setup() {
  // função para conectar ao wi-fi definido anteriormente
  conectarWifi();
  // função para utilizar o server definido anteriormente, para porta 1883
  client.setServer(mqtt_Broker, 1883);
}

// --- MAIN ---
// mantém sistema rodando
void loop() {
  // caso a conexão não aconteça~
  if (!client.connected()) {
    // função de reconectar ao MQTT será chamada para que a conexão seja realizada
    reconectarMQTT();}
  // função para que o sensor utilizado meça os dados
  medirDados();
  // função para enviar as informações ao tópico
  publicarDadosNoTopico();
}

// função para iniciar a tentativa de conectar ao wi-fi 
void conectarWifi() {
  // espera de segurança
  delay(10);

  // iniciar a conexão wi-fi na rede ssid com a senha password
  WiFi.begin(ssid, password);
}

// função para reconeção com o servidor
void reconectarMQTT() {
    // enquanto o cliente não estiver conectado o pedido de conexão do cliente será chamado
    while (!client.connected()) {
    client.connect(mqtt_ClientID);
  }
}

// função para enviar os dados do sensor para seu tópico
void publicarDadosNoTopico() {
  // serão puclicados e mantidos no tópico de temperatura seus respectivos dados
  client.publish(topicoTemperatura, String(temperatura).c_str(), true);
  // serão puclicados e mantidos no tópico de umidade seus respectivos dados
  client.publish(topicoUmidade, String(umidade).c_str(), true);
  // espera entre as postagens
  delay(5000);
}

// função para que o sensor meça os dados
void medirDados() {
  // atribuição do valor medido a sua respectiva variável de umidade
  umidade = dht.readHumidity();
  // atribuição do valor medido a sua respectiva variável de temperatura
  temperatura = dht.readTemperature(false);
  // tempo de espera entre as medições
  delay(2500);
}
