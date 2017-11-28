//Trabalho de graduação - WebSensor - Gabriel Dornelas dos Santos

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
const char* topicoTemperatura = "sensor/temperatura";
// nomeando tópico de umidade do servidor
const char* topicoUmidade = "sensor/umidade";

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

/*// --- DISPLAY ---
// biblioteca para utilizar o display
#include <Adafruit_SSD1306.h>
// definição para utilização do led da placa nodemcu
#define OLED_RESET LED_BUILTIN
// disponibiliza o uso do display
Adafruit_SSD1306 display(OLED_RESET);*/

// --- BOOT ---
// inicia o sistema
void setup() {
  // função de iniciar o display
  //configurarDisplay();
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
  // mostrar no display os dados medidos
  //mostrarDados();
  // função para enviar as informações ao tópico
  publicarDadosNoTopico();
  delay(60000);
}

// função para mostrar no display a tentativa de conectar ao wi-fi 
void conectarWifi() {
  // espera de segurança
  delay(10);

  // definição de tamanho de fonte para o display
  /*display.setTextSize(2);
  // definição do local da mensagem a ser apresentada no display
  display.setCursor(0, 0);
  // mensagem a ser enviada ao display
  display.print("Conectando ");
  // enviar mensagem ao display com as configurações definidas
  display.display();*/

  // iniciar a conexão wi-fi na rede ssid com a senha password
  WiFi.begin(ssid, password);

  // enquanto o wi-fi não for conectado~
  while (WiFi.status() != WL_CONNECTED) {
    // a cada segundo um ponto será mostrado no display
    delay(1000);
    /*display.print(".");
    display.display();*/
  }
}

// função para reconeção com o servidor
void reconectarMQTT() {
    // enquanto o cliente não estiver conectado o pedido de conexão do cliente será chamado
    while (!client.connected()) {
    client.connect(mqtt_ClientID);
  }
}

/*// função para configuração e utilização do display
void configurarDisplay() {
  // função do display para seu uso
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  // definição da cor da fonte a ser apresentada no display
  display.setTextColor(WHITE);
  // limpa dados que haviam no display
  display.clearDisplay();
  // definição de tamanho de fonte para o display
  display.setTextSize(5);
  // definição do local da mensagem a ser apresentada no display
  display.setCursor(0, 0);
  // mensagem inicial a ser enviada ao display
  display.print("Bem-vindo !");
  // enviar mensagem ao display com as configurações definidas
  display.display();
  // tempo para que a leitura da mensagem seja compreendida
  delay(1500);
  // limpa dados que haviam no display
  display.clearDisplay();
}*/

// função para enviar os dados do sensor para seu tópico
void publicarDadosNoTopico() {
  // serão puclicados e mantidos no tópico de temperatura seus respectivos dados
  client.publish(topicoTemperatura, String(temperatura).c_str(), true);
  // serão puclicados e mantidos no tópico de umidade seus respectivos dados
  client.publish(topicoUmidade, String(umidade).c_str(), true);
}

// função para que o sensor meça os dados
void medirDados() {
  // atribuição do valor medido a sua respectiva variável de umidade
  umidade = dht.readHumidity();
  // atribuição do valor medido a sua respectiva variável de temperatura
  temperatura = dht.readTemperature(false);
  // tempo de espera entre as medições
  delay(5000);
}

/*// função para mostrar os dados no display
void mostrarDados() {
  // mostra os dados de temperatura
  mostrarMensagemNoDisplay("Temperatura", (temperatura), " C");
  // mostra os dados de umidade
  mostrarMensagemNoDisplay("Umidade", (umidade), " %");
}*/

/*// função para mostrar mensagem dos valores medidos no display
void mostrarMensagemNoDisplay(const char* texto1, int medicao, const char* texto2) {
  // limpa dados que haviam no display
  display.clearDisplay();
  // definição de tamanho de fonte para o display
  display.setTextSize(1);
  // definição do local da mensagem a ser apresentada no display
  display.setCursor(0, 0);
  // primeira mensagem recebida pela função a ser enviada ao display
  display.print(texto1);
  // definição de tamanho de fonte para o display
  display.setTextSize(5);
  // definição do local da mensagem a ser apresentada no display
  display.setCursor(20, 20);
  // valor do dado da primeira mensagem recebida pela função a ser enviada ao display
  display.print(medicao);
  // definição de tamanho de fonte para o display
  display.setTextSize(2);
  // segunda mensagem recebida pela função a ser enviada ao display
  display.print(texto2);
  // enviar mensagem ao display com as configurações definidas
  display.display();
  // tempo para que a leitura da mensagem seja compreendida
  delay(2000);
}*/
