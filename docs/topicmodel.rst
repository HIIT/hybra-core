LDA topic modeling with Hybra-core and CSC
==========================================

The collection of scripts included with Hybra-core in the /hybra/analysis/topicmodel/ directory can be used to create LDA (Latent Dirichlet Allocation) topic models on the Taito super cluster of CSC (IT Center for Science). To do this, the user needs an account with which to use CSC's services. See `https://www.csc.fi <https://www.csc.fi>`_ for more information and also to familiarize yourself with using Taito and CSC's services in general.

Assuming that the user has access to Taito, has setup the scripts on and has moved the data to Taito, this manual explains how to use the various scripts to create an LDA model. This manual and the scripts used assume that the data has been saved as one document (or unit of analysis) per file. It is probably a good idea to name the files with a message ID or something similar so that they can be identified later on.

Step 1: Lemmatizing
*******************

The script lemmatize.py can be used to lemmatize the words in the documents, i.e. to infer their dictionary form.  While not strictly necessary, this probably enhances the quality of the resulting topic model by attempting to group together the many forms of Finnish words. The script relies on CSC's finnish-process lemmatizer. The script also performs basic cleaning of the data set, by removing URLs and most punctuation. When working with other than Finnish-language data, this step can be skipped, but data cleaning and lemmatizing/stemming will have to be done in some other way.

There are two batch scripts that can be used to start the lemmatizing script, lemma.batch and array_lemma.batch. Array_lemma.batch divides the corpus into 200 parts and works on them in parallel, speeding the process up significantly, and is thus recommended if the number of files is large. Whichever version you use, you should edit the batch file to point to the correct directory and possibly tweak the CPU and memory requirements, then start it with 'sbatch _file_.batch'.

The script writes the lemmatized versions of the documents in the same directory as the original files and names them as original_name.lemma, so e.g. the lemmatized version of tweet_id.txt is tweet_id.txt.lemma. Before the next part, you should move the lemmatized files to another directory.

Step 2: Creating the DTM
************************

The next step is to create the DTM (document-term matrix) using the script create_dtm.r. For example, by loading the R environment with 'module load r-env' and using Rscript to run the script as 'Rscript create_dtm.r /path/to/lemmas/'.

The DTM is saved in a file called dtm.rdata within the same folder as the documents used to create it. Move it to wherever you want to use it.

Step 3: Creating the LDA model
******************************

The script create_topics.r takes as parameters a path to the DTM and a number *k*, which refers to the number of topics to be included in the model. The script can be used on its own, but the preferred way is to use the batch file topicmodel.batch to handle the task. Topicmodel.batch will (by default) actually create a model for each *k* from 2 to 300 in parallel. Tweak the memory and time requirements and the range of *k*s to use as necessary and edit the file to point to the correct path.

Note that creating the models with the largest *k*s usually takes most of the time, while creating smaller models is relatively fast. If some of the arrays run out of time, you can simply create those models later without the whole batch job again.

The end result is a collection of files, named topic-*k*.rdata, located within the same directory as the DTM.

Step 4: Finding the best K
**************************

The script check_k.r can be used to find the model with the 'optimal' number of topics among those just created, using harmonic log-likelihood (see ref). Unfortunately, the script depends on versions of R packages not present on CSC's servers, so the topic models will have to be moved somewhere else for this part.

The script takes as an argument a path to the directory with the topic models. The optional argument --plot will cause the script to plot a curve of the log-likelihoods. The script will print the 'best' model and the corresponding score.

The end result is a topic model that you can then inspect using R. See the `documentation <https://www.google.fi/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwjLk_Dbnb7YAhVEYlAKHQtoBlwQFggsMAA&url=https%3A%2F%2Fcran.r-project.org%2Fpackage%3Dtopicmodels&usg=AOvVaw2iq6Xg34iOC9NL4kJZHgLV>`_ of the R package 'topicmodels' for more information.

Troubleshooting
***************

This section attempts to address some common problems encountered during the process.

Some files were not lemmatized
------------------------------

This can happen for various reasons, such as the process running out of time and memory. You can use CSC's tools such as the command 'sacct' to see if one of the array jobs failed and for what reason.

It is also possible, for example, that a bug in the lemmatizer is causing it to freeze when working on certain files. This has earlier happened when processing certain types of URLs, but this should have been fixed. If you determine that this is the case, please file a bug report on GitHub or contact us.

Argument length too long' error when moving or copying files
------------------------------------------------------------

If the number of files is large, simply using 'mv' to move them won't work. In this case one may combine mv with 'find'. The basic command to use is as follows (assuming you have the the original documents in directory texts within the parent directory *d* and want to move them to sibling directory _lemma_), given from within *d*:

find text -name '*.lemma' -exec mv -t lemma {} +;

Some topic models were not generated
------------------------------------

This is probably because of insufficient computation time or memory. Tweak them and try again.
