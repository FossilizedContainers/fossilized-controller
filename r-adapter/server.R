# All the libraries needed. httpuv required Rook, request, and httr.
http.libraries = c("httpuv",
                   "Rook", "request", "httr",
                   "remotes")

for ( pkg in http.libraries ) {
  if ( !requireNamespace(pkg) ) {
    install.packages(pkg)
  }
}

# install lipdR library using remotes package
# remotes::install_github("nickmckay/LiPD-Utilities", subdir = "R", quiet = TRUE)

# load in lipdR package
library("lipdR")


# load in httpuv package
library("httpuv")



# Usage:
# 
# Run source on the file. If lipdR is not installed, uncomment line 17 to 
# install the lipdR library with the remotes package. The remotes package should
# already be installed after you've run source.
#
# To START the httpuv server, enter "httpuv.server" in the R console
#
# To STOP the httpuv server, enter "stopAllServers()" in the R console
# 
# To LIST ALL running httpuv servers, enter "listServers()" in the R console



# Information About httpuv Programs:
#
# req from call(req) is built on from Rook. This link below provides more info 
# on req's fields on page 3 under the "The Environment" section:
#       https://cran.r-project.org/web/packages/Rook/Rook.pdf
# 
# Also includes additional field HEADERS just for the httpuv package. Here is an
# example output:
#       accept 
#         "*/*" 
#       accept-encoding 
#         "gzip, deflate" 
#       connection 
#         "keep-alive" 
#       content-length 
#         "12045" 
#       content-type 
#         "multipart/form-data; boundary=344d170547b298b23acea1965702db19" 
#       host 
#         "127.0.0.1:4000" 
#       user-agent 
#         "python-requests/2.26.0"

httpuv.server <- startServer(host = "127.0.0.1", 
                             port = 4000,
                             list(
                               call = 
                                 function(req) {
body = NULL
                                   
if (req$REQUEST_METHOD == "POST") {
  parse.results = parse_multipart(req)
  
  body = paste0(body, "Results of file upload via POST:")
  
  for (part in parse.results) {
    # read file back in with lipidR functions
    #
    # NOTE:
    #
    # If there's an error, the console prints out the error message for 
    # readLipd() and returns an empty list
    read.lipd.result <- list(readLipd(part$filename))

    check.string <- ifelse(length(read.lipd.result), 
                           " ... uploaded successfully",
                           " ... readLipd error")
    
    body = paste0(body, "<br>", part, check.string)
  }
}
  
  
if (is.null(body)) {
  body = paste0("Time: ", Sys.time(), "<br>Path requested: ", req$PATH_INFO)  
}
                                   
  
ret = list(status = 200L,
           headers = list('Content-Type' = 'text/html'),
           body = body)

return(ret)
}))


# Utility Functions: parse_multipart

# Borrows heavily from the parse function in the Rook's package /R/utils.R file. 
# This function parses and saves a file or files in a POST request's form data 
# in the current working directory.
#
# NOTE:
#   * EASY ACCESS POINT to: "CHANGE WHERE THE FILE IS SAVED", 
#   * Specific values in the comments will not apply in all situations, i.e. 
#           the values derived from the POST request are subject to change
parse_multipart = function(env){
  
  # check if env is empty
  if (!exists('CONTENT_TYPE', env)) return(NULL)
  
  params  <- list()
  
  # Grab the InputStream and rewind it to the start; 
  # Because of an error, we can't access the input directly outside of the 
  # httpuv server: 
  #     Error in seek.connection(private$conn, 0) : invalid connection
  input <- env$`rook.input`
  input$rewind()
  
  # content_length = 12063L
  content_length = as.integer(env$CONTENT_LENGTH)
  
  # Bail if not a multipart content body
  if (!grepl('multipart', env$CONTENT_TYPE)) return(NULL)
  
  
  # File extensions that should be saved in binary
  binary.file.exts = c(".lpd", ".cdf")
  
  # Some constants regarding boundaries and a buffer environment to read the 
  # data into
  
  # EOL aka End of Line
  # EOL is defined in Rook::Utils as part of the Multipart class; it is a 
  # CRLF or Carriage Return + Line Feed.
  EOL <- "\r\n"
  
  # boundary = "--8a3020e016cd8d412a3722d8d10edfd0"
  #
  # According to RFC 1341, section 7.2.1, an HTTP request with Content-Type:
  # "multipart" is where the body contains many parts. A part, in our case, 
  # would be a file. Each part is prepended by an "encapsulation boundary" 
  # with the last part appended by a "closing boundary". 
  #
  # The boundary in which the encapsulation and closing boundary are based on 
  # is specified in the Content-Type header field under the "boundary" 
  # parameter. Here is what it looks like for our POST request:
  #
  #   Content-Type: multipart/form-data; 
  #                   boundary=8a3020e016cd8d412a3722d8d10edfd0
  # 
  # The encapsulation line is the boundary parameter prepended by two '-'
  # as seen in the boundary variable. It must be at the beginning of a line.
  # It follows a CRLF, and is followed by an additional CRLF with header fields
  # for the part or by 2 CRLFs for Content-Type: text/plain.
  #
  # The encapsulation boundary is CRLF + encapsulation line.
  #
  # The closing boundary is the boundary parameter prepended and appended by 
  # two '-' on each side, with a CRLF prepended to by the beginning 2 dashes 
  # e.g.:
  #
  #   "\r\n--8a3020e016cd8d412a3722d8d10edfd0--"
  #
  # 
  #
  # According to RFC 7578, "multipart/form-data" is formatted slightly 
  # differently than other multipart types.
  #
  # Each part has to have a Content-Disposition header field where the 
  # disposition type is "form-data". There must be a parameter "name". If the
  # the form data is the contents of a file, there must be a parameter 
  # "filename":
  #
  #   Content-Disposition: form-data; name="user"; filename="user.docx"
  #
  # After the header fields, there are 2 CRLFs then the part's data or body. The
  # in our case, will be file data. 
  #
  # So roughly, the format of multipart/form-data is:
  #   
  #   encapsulation boundary + CRLF
  #   header fields + CRLF + CRLF
  #   body + CRLF
  #   encapsulation boundary + CRLF
  #   header fields + CRLF + CRLF
  #   closing boundary + CRLF
  boundary <- paste('--',
                    gsub('^multipart/.*boundary="?([^";,]+)"?',
                         '\\1',
                         env$CONTENT_TYPE,perl=TRUE),sep='')
  
  # boundary_size = 34L
  #
  # The bytesize function returns the number of bytes needed to store the 
  # argument
  boundary_size <- Rook::Utils$bytesize(boundary)
  
  # boundaryEOL = "--8a3020e016cd8d412a3722d8d10edfd0\r\n"
  boundaryEOL <- paste(boundary,EOL,sep='')
  
  # boundaryEOL_size = 36L
  boundaryEOL_size <- boundary_size + Rook::Utils$bytesize(EOL)
  
  #  EOLEOL =  "\r\n\r\n"
  EOLEOL = paste(EOL,EOL,sep='')
  
  # EOLEOL_size = 4L
  EOLEOL_size = Rook::Utils$bytesize(EOLEOL)
  
  # EOL_size = 2L
  EOL_size = Rook::Utils$bytesize(EOL)
  
  
  # new.env is a function from the base R package that creates a new 
  # environment. Environments in R have a lot of interesting uses and is how the 
  # Rook's HTTP requests are stored
  buf <- new.env()
  buf$bufsize <- 16384 # Never read more than bufsize bytes.
  
  # buf$read_buffer = 2d 2d 38 61 33 30 32 30 65 30 31 36 63 64 38 64 34 31 32 
  #                   61 33 37 32 32 64 38 64 31 30 65 64 66 64 30 0d 0a
  #                   OR 
  #                   --8a3020e016cd8d412a3722d8d10edfd0\r\n (in bytes)
  # 
  # This is the 1st of 2 places that read from the input; The read function 
  # returns the number of bytees specified in the argument, in this case 
  # boundaryEOL_size
  buf$read_buffer <- input$read(boundaryEOL_size)
  
  # buf$read_buffer_len = 36
  buf$read_buffer_len <- length(buf$read_buffer)
  
  # buf$unread = 20944
  buf$unread <- content_length - boundary_size 
  
  # i = 1 if input formatted correctly.
  #
  # Rook::Utils$raw.match is a function that takes 2 arguments. The first, the
  # needle, is a character or raw vector while the second, the haystack, is 
  # always a raw vector.
  #
  # The function returns the first place / index where the needle was found in 
  # the stack. If the first place is where the needle occurs in the haystack,
  # then 1 is returned. If there is no needle in the haystack, then 0 is 
  # returned.
  i <- Rook::Utils$raw.match(boundaryEOL,buf$read_buffer,all=FALSE)
  
  # Checks if boundaryEOL are the first bytes received from the input after 
  # reading in the size of boundaryEOL. Because of how Multipart is specified, 
  # the first bytes should always be the boundary + EOL.
  if (!length(i) || i != 1){
    warning("bad content body")
    input$rewind()
    return(NULL)
  }

    

  # Helper functions to use later on: fill_buffer, slice_buffer
  
  # fill_buffer reads in a number of bytes into the x environment. The
  # number of bytes is either x's bufsize or x's unread, whichever is smaller.
  #
  # The new bytes are appended to x's read_buffer. Then read_buffer_len and 
  # unread variables in the x environment are updated.
  #
  # This is the 2nd of 2 places that read from the input.
  fill_buffer <- function(x){
    buf <- input$read(ifelse(x$bufsize < x$unread, x$bufsize, x$unread))
    buflen <- length(buf)
    
    if (buflen > 0){
      x$read_buffer <- c(x$read_buffer,buf)
      x$read_buffer_len <- length(x$read_buffer)
      x$unread <- x$unread - buflen
    }
  }
  
  # slice_buffer is used usually in conjuction with Rook::Utils$raw.match to 
  # find a specific string, set read_buffer to point after that string, and
  # return the bytes that were before that string. 
  #
  # In R's byte subscription the first position is 1. Zero is usually ignored 
  # for R subscripts.
  #
  # i is the place in read_buffer where a certain string appeared. size is the 
  # the size in bytes of that certain string. x is the buffer environment.
  #
  # If i is greater than 1, then slice will be all the bytes before index i in 
  # x's read_buffer. If i is equal to or less than 1, then slice will be the 
  # first byte in x's read_buffer.
  #
  # If size is less than x's read_buffer_len, then x's read_buffer is all bytes 
  # at and after position i + size. If size is equal to or greater than x's 
  # read_buffer, then x's read_buffer is set to raw(0).
  # 
  # x's read_buffer_len is updated to reflect the changes to read_buffer and 
  # slice is returned.
  slice_buffer <- function(i, size, x){
    slice <- 
      if(i > 1) { 
        x$read_buffer[1:(i - 1)] 
      } else { 
        x$read_buffer[1] 
      }
    
    x$read_buffer <-
      if(size < x$read_buffer_len) { 
        x$read_buffer[(i + size):x$read_buffer_len] 
      } else { 
        raw()
      }
    
    x$read_buffer_len <- length(x$read_buffer)
    slice
  }
  
  
  
  ### prime the read_buffer
  
  # buf$read_buffer = raw(0)
  buf$read_buffer <- raw()
  
  # buf$read_buffer = first (bufsize or unread) number of bytes, buf$unread and
  # buf$read_buffer_len are updated
  fill_buffer(buf)
  
  
  
  # Loop that looks for a parts and the closing boundary 
  while(TRUE) {
    head <- value <- NULL
    filename <- content_type <- name <- NULL
    
    
    while(is.null(head)){
      # At this point the buffer is pointing after the first CRLF of the 
      # encapsulating boundary. What follows should be a CRLF and then the 
      # part's header fields.
      #
      # We're looking for the end of this current part's header fields. Every 
      # part's header fields ends with 2 CRLFs as mentioned above in the 
      # boundary declaration comment block.
      #
      # The raw.match function will return the place where 2 consecutive CRLFs 
      # occur in the read_buffer.
      i <- Rook::Utils$raw.match(EOLEOL,buf$read_buffer,all=FALSE)
      
      # If i is not 0 aka 2 consecutive CRLFs were found, then slice the buffer;
      #
      # Else if there are still bytes to be read, fill the buffer again.
      #
      # Else, we were unable to find a valid head.
      if (length(i)){
        head <- slice_buffer(i,EOLEOL_size,buf)
        break
      } else if (buf$unread){
        fill_buffer(buf)
      } else {
        break ### we've read everything and still haven't seen a valid head
      }
    }
    
    # If there isn't a valid head, error out
    if (is.null(head)){
      warning("Bad post payload: searching for a header")
      input$rewind()
      return(NULL)
    }
    
    
    
    ### cat("Head:",rawToChar(head),"\n")
    ### they're 8bit clean
    
    # Parsing the header fields
    head <- rawToChar(head)
    token <- '[^\\s()<>,;:\\"\\/\\[\\]?=]+'
    condisp <- paste('Content-Disposition:\\s*',token,'\\s*',sep='')
    dispparm <- paste(';\\s*(',token,')=("(?:\\"|[^"])*"|',token,')*',sep='')
    rfc2183 <- paste('(?m)^',condisp,'(',dispparm,')+$',sep='')
    broken_quoted <- paste('(?m)^',condisp,'.*;\\sfilename="(.*?)"(?:\\s*$|\\s*;\\s*',token,'=)',sep='')
    broken_unquoted = paste('(?m)^',condisp,'.*;\\sfilename=(',token,')',sep='')
    
    if (length(grep(rfc2183, head, perl=TRUE))){
      first_line <- sub(condisp,'', strsplit(head, '\r\n')[[1L]][1], perl=TRUE)
      pairs <- strsplit(first_line, ';', fixed=TRUE)[[1L]]
      fnmatch <- '\\s*filename=(.*)\\s*'
      
      if (any(grepl(fnmatch, pairs, perl=TRUE))){
        filename <- pairs[grepl(fnmatch, pairs, perl=TRUE)][1]
        filename <- gsub('"', '', sub(fnmatch, '\\1', filename, perl=TRUE))
      }
    } else if (length(grep(broken_quoted, head, perl=TRUE))){
      filename <- sub(broken_quoted, '\\1', strsplit(head, '\r\n')[[1L]][1], perl=TRUE)
    } else if (length(grep(broken_unquoted, head, perl=TRUE))){
      filename <- sub(broken_unquoted, '\\1', strsplit(head,'\r\n')[[1L]][1], perl=TRUE)
    }
    
    if (!is.null(filename) && filename != ''){
      filename = Rook::Utils$unescape(filename)
    }
    
    headlines <- strsplit(head, EOL, fixed=TRUE)[[1L]]
    content_type_re <- '(?mi)Content-Type: (.*)'
    content_types <- headlines[grepl(content_type_re, headlines, perl=TRUE)]
    
    if (length(content_types)){
      content_type <- sub(content_type_re, '\\1', content_types[1], perl=TRUE)
    }
    
    name <- sub('(?si)Content-Disposition:.*\\s+name="?([^";]*).*"?', '\\1', head, perl=TRUE)
    
    
    
    # Find the start of the next boundary, encapsulating or closing, and save 
    # the current body in the current working directory.
    while(TRUE){
      i <- Rook::Utils$raw.match(boundary, buf$read_buffer, all=FALSE)
      
      # If you can find a valid boundary, parse the part
      if (length(i)){
        value <- slice_buffer(i, boundary_size, buf)
        
        if (length(value)){
          ### Drop EOL only values
          if (length(value) == 2 && length(Rook::Utils$raw.match(EOL, value))) { 
            break
          }
          
          if (!is.null(filename) || !is.null(content_type)){
            data <- list()
            
            if (!is.null(filename)) {
              data$filename <- strsplit(filename, '[\\/]', perl=TRUE)[[1L]]
            }
            
            if (!is.null(content_type)) {
              data$content_type <- content_type
            }
            
            data$head <- head
            
            # CHANGE WHERE THE FILE IS SAVED
            con <- file(data$filename, open='wb')
            
            writeBin(value,con)
            close(con)
            
            params[[name]] <- data
          } else {
            len <- length(value)
            
            # Trim trailing EOL
            if (len > 2 && length(Rook::Utils$raw.match(EOL, value[(len-1):len], all=FALSE))) {
              len <- len -2
            }
            
            # Handle array parameters
            paramValue <- Rook::Utils$escape(rawToChar(value[1:len]))
            paramSet <- FALSE
            
            if (grepl("\\[\\]$", name)) {
              name <- sub("\\[\\]$", "", name)
              
              if (name %in% names(params)) {
                params[[name]] <- c(params[[name]], paramValue)
                paramSet <- TRUE
              }
            }
            
            if (!paramSet) { params[[name]] <- paramValue }
          }
        }
        break
      } else if (buf$unread){ # The boundary isn't currently in read_buffer 
                              # but still can be further down the input stream
        fill_buffer(buf) 
      } else { # We've read everything and still haven't seen a boundary
        break  
      }
    }
    
    # Bad post payload
    if (is.null(value)){ 
      input$rewind()
      warning("Bad POST payload: Searching for a body part")
      return(NULL)
    }
    
    # Now search for ending markers or the beginning of another part
    while (buf$read_buffer_len < 2 && buf$unread) { fill_buffer(buf) }
    
    # Bad stuff at the end. just return what we've got and presume everything is 
    # okay
    if (buf$read_buffer_len < 2 && buf$unread == 0){
      input$rewind()
      return(params)
    }
    
    # We've found a valid closing boundary ending
    if (length(Rook::Utils$raw.match('--', buf$read_buffer[1:2], all=FALSE))){
      input$rewind()
      return(params)
    }
    
    # Skip past the EOL
    if (length(Rook::Utils$raw.match(EOL, buf$read_buffer[1:EOL_size], all=FALSE))){
      slice_buffer(1, EOL_size, buf)
    } else {
      warning("Bad POST body: End of Line (\r\n) not present")
      input$rewind()
      return(params)
    }
    
    # Another sanity check before we try to parse another part; if the buffer 
    # and unread byte length is less than the boundary size, then there isn't a
    # proper ending to the POST payload
    if ((buf$read_buffer_len + buf$unread) < boundary_size){
      warning("Bad POST body: Unknown trailing bytes")
      input$rewind()
      return(params)
    }
  } # end of while from line 378
}