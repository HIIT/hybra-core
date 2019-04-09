Prerequisite

Yopu need to have a SeCo lexical analysis service running.

More details, see: https://github.com/jiemakel/las-ws

If you install it as a Docker installation, this command starts and binds the codebase correctly: docker run -p 127.0.0.1:19990:9000 jiemakel/las-ws:1.1 .

This is required to lemmatize content for topic models.

Running

core.plugin( 'plugin/stm/stm',
  data = d,
  k = 2,
  saveto = '~/temp/results/' )

Parameters

data HYBRA core compatible data, i.e., a list of dictonaries with keys such as text_content and timestamp.

k the number of topics to extract from the material. Following STM guidelines, set to zero to optimize it.

saveto folder where outputs (like lemmatized data and topicmodel objects) are stored.

lasserver address to the SeCo lexical analysis service server.
