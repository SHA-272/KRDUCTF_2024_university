void setup()
{
  Serial.begin(9600);
  char key[] = "\x13\x37\x20\x24";
  char encrypted_text[] = "xEDQh[\x13\x17gh\x14VwB\x11J#h\x11WL\x03M\x10i\x06NCn";

  char decrypted_text[sizeof(encrypted_text)];
  int text_length = strlen(encrypted_text);
  int key_length = strlen(key);

  for (int i = 0; i < text_length; i++)
  {
    decrypted_text[i] = encrypted_text[i] ^ key[i % key_length];
  }d:\MyFiles\CTF\KRDUCTF_2024_university\reverse\ino_2\src\sketch\sketch.ino
  Serial.println("Flag:");
  Serial.println(decrypted_text);
}

void loop()
{
}
