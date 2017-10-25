//Trabalho de graduação - WebSensor - Gabriel Dornelas dos Santos

// --- WIFI ---
#include <ESP8266WiFi.h> // biblioteca para uso do wi-fi
const char* ssid = "Gabriel"; // troque pelo nome da sua rede
const char* password = "danigamel"; // troque pela senha da sua rede
WiFiClient nodemcuClient; // objeto para conexão do wi-fi

// --- MQTT ---
#include <PubSubClient.h> // biblioteca para uso do servidor MQTT
const char* mqtt_Broker = "iot.eclipse.org"; // endereço do servidor
const char* mqtt_ClientID = "Gabriel"; // nome do cliente para acessar o servidor
PubSubClient client(nodemcuClient); // criando o servidor
const char* topicoTemperatura = "sensor/temperatura"; // nomeando tópico de temperatura do servidor
const char* topicoUmidade = "sensor/umidade"; // nomeando tópico de umidade do servidor

// --- DHT ---
#include <DHT.h> // biblioteca para uso do sensor de temperatura/umidade
#define DHTPIN D3 // definição do pino a ser utilizado na placa nodemcu
#define DHTTYPE DHT11 // definição do modelo do sensor a ser utilizado
DHT dht(DHTPIN, DHTTYPE); // função para utilizar o sensor
int umidade; // variável onde será armazenado dado de umidade
int temperatura; // variável onde será armazenado dado de temperatura

// --- DISPLAY ---
#include <Adafruit_SSD1306.h> // biblioteca para utilizar o display
#define OLED_RESET LED_BUILTIN // definição para utilização do led da placa nodemcu
Adafruit_SSD1306 display(OLED_RESET); // disponibiliza o uso do display

// --- BOOT ---
void setup() { // inicia o sistema
  configurarDisplay(); // função de iniciar o display
  conectarWifi(); // função para conectar ao wi-fi definido anteriormente
  client.setServer(mqtt_Broker, 1883); // função para utilizar o server definido anteriormente, para porta 1883
}

// --- MAIN ---
void loop() { // mantém sistema rodando
  if (!client.connected()) { // caso a conexão não aconteça~
    reconectarMQTT(); 		 // função de reconectar ao MQTT será chamada para que a conexão seja realizada
  }
  medirDados(); // função para que o sensor utilizado meça os dados
  mostrarDados(); // mostrar no display os dados medidos
  publicarDadosNoTopico(); // função para enviar as informações ao tópico
}

void conectarWifi() { // função para mostrar no display a tentativa de conectar ao wi-fi 
  delay(10); // espera de segurança

  display.setTextSize(2); // definição de tamanho de fonte para o display
  display.setCursor(0, 0); // definição do local da mensagem a ser apresentada no display
  display.print("Conectando "); // mensagem a ser enviada ao display
  display.display(); // enviar mensagem ao display com as configurações definidas

  WiFi.begin(ssid, password); // iniciar a conexão wi-fi na rede ssid com a senha password

  while (WiFi.status() != WL_CONNECTED) { // enquanto o wi-fi não for conectado~
    delay(1000);						  // a cada segundo~
    display.print(".");					  // um ponto será mostrado~
    display.display();					  // no display
  }
}

void reconectarMQTT() { // função para reconeção com o servidor
  while (!client.connected()) {		// enquanto o cliente não estiver conectado~
    client.connect(mqtt_ClientID);	// o pedido de conexão do cliente será chamado
  }
}

void configurarDisplay() { // função para configuração e utilização do display
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C); // função do display para seu uso
  display.setTextColor(WHITE); // definição da cor da fonte a ser apresentada no display
  display.clearDisplay(); // limpa dados que haviam no display
  display.setTextSize(5); // definição de tamanho de fonte para o display
  display.setCursor(0, 0); // definição do local da mensagem a ser apresentada no display
  display.print("Bem-vindo !"); // mensagem inicial a ser enviada ao display
  display.display(); // enviar mensagem ao display com as configurações definidas
  delay(1500); // tempo para que a leitura da mensagem seja compreendida
  display.clearDisplay(); // limpa dados que haviam no display
}

void publicarDadosNoTopico() { // função para enviar os dados do sensor para seu tópico
  client.publish(topicoTemperatura, String(temperatura).c_str(), true); // serão puclicados e mantidos no tópico de temperatura seus respectivos dados
  client.publish(topicoUmidade, String(umidade).c_str(), true); // serão puclicados e mantidos no tópico de umidade seus respectivos dados
}

void medirDados() { // função para que o sensor meça os dados
  umidade = dht.readHumidity(); // atribuição do valor medido a sua respectiva variável de umidade
  temperatura = dht.readTemperature(false); // atribuição do valor medido a sua respectiva variável de temperatura
  delay(5000); // tempo de espera entre as medições
}

void mostrarDados() { // função para mostrar os dados no display
  mostrarMensagemNoDisplay("Temperatura", (temperatura), " C"); // mostra os dados de temperatura
  mostrarMensagemNoDisplay("Umidade", (umidade), " %"); // mostra os dados de umidade
}

void mostrarMensagemNoDisplay(const char* texto1, int medicao, const char* texto2) { // função para mostrar mensagem dos valores medidos no display
  display.clearDisplay(); // limpa dados que haviam no display
  display.setTextSize(1); // definição de tamanho de fonte para o display
  display.setCursor(0, 0); // definição do local da mensagem a ser apresentada no display
  display.print(texto1); // primeira mensagem recebida pela função a ser enviada ao display
  display.setTextSize(5); // definição de tamanho de fonte para o display
  display.setCursor(20, 20); // definição do local da mensagem a ser apresentada no display
  display.print(medicao); // valor do dado da primeira mensagem recebida pela função a ser enviada ao display
  display.setTextSize(2); // definição de tamanho de fonte para o display
  display.print(texto2); // segunda mensagem recebida pela função a ser enviada ao display
  display.display(); // enviar mensagem ao display com as configurações definidas
  delay(2000); // tempo para que a leitura da mensagem seja compreendida
}