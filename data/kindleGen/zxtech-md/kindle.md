# Kindle

## <a name="overview">Overview</a>

Kindle is a brand name from Amazon. 
It can represent either:

1. electronic books that are files formatted in Amazon's proprietary formats (MOBI or KF)  
These are also known as Kindle ebooks.  
These files typically have the file extensions `.mobi` or `.kf8` for their respective format.
1. electronic devices for reading Kindle ebooks

The rest of this section describes how one would make an Kindle ebook.

## <a name="steps"></a>Steps to make Kindle ebook

The file format of a Kindle ebook is proprietary to Amazon.  
Hence, there is no easy way to generate one from scratch.  
Amazon does provide tools for authors to convert works in other document formats such as HTML and XHTML or ebook formats (such as `EPUB`, `FB2` or `XMDF`) into their `.mobi` format.

## <a name="kindle-format"></a>Kindle format


The `.mobi` format files was developed by Mobipocket SA for the MobiPocket Reader. The company was bought over by Amazon which adopted the format for their ebook reading devices.

The `.kf8` format is an enhanced version the `.mobi` format. It was intended to replace `.mobi`. It is backwards compatibility with most older generation of Amazon Kindle readers except for 1st & 2nd Generation Kindle devices and Kindle DX.

## <a name="tools">Tools</a>

There are 2 conversion tools provided by Amazon to convert existing content into Kindle format.

1. [Kindle Create](https://kdp.amazon.com/en_US/help/topic/G200735480)
   ([https://kdp.amazon.com/en_US/help/topic/G200735480](https://kdp.amazon.com/en_US/help/topic/G200735480))  
   This application takes in a `.docx` or `.pdf` file and convert it to Kindle format. Although this tool provides a user-interface, I do not find it to be user-friendly tool. I find myself spending a lot of time tweaking the file and then converting it and then to preview it.

1. [KindleGen](https://www.amazon.com/gp/feature.html?ie=UTF8&docId1000765211)    ([https://www.amazon.com/gp/feature.html?ie=UTF8&docId1000765211](https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765211))  
   This is a command-line tool takes in HTML document or existing ebooks in other formats (EPUB) and convert them to Kindle format. The rest of the 

If you are using KindleGen, another useful tool would be [Kindle Previewer](https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765261) ([https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765261](https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765261)).  
This tool allows you to preview the `.mobi` file that was generated.  
Unfortunately, this tool is only available on Windows and MacOS.  

If you are using Kindle Create, you do not need Kindle Previewer (its packaged within the app).

