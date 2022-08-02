#!/usr/bin/env Rscript

args<-commandArgs(TRUE)

if (length(args)==0) {
  input = Sys.getenv("AVG_INPUT", "input.pptx")
  output = Sys.getenv("AVG_OUTPUT", paste(input, "mp4", sep="."))
} else {
  input = args[1]
  output = args[2]
}
print(input)
print(output)

markdown = paste(input, "md", sep=".")
service = Sys.getenv("AVG_SERVICE", "amazon")
voice = Sys.getenv("AVG_VOICE", "Matthew")
dpi = as.double(Sys.getenv("AVG_DPI", 300))
subtitles = Sys.getenv("AVG_SUBTITLES", "TRUE")
verbose = Sys.getenv("AVG_VERBOSE", "TRUE")

doc <- ariExtra::pptx_to_ari(
  input,
  dpi = dpi,
  output = markdown
)

doc[c("images", "script")]
script = doc$script
slides = doc$images

result <- ari::ari_spin(slides, script,
  output = output,
  service = service,
  voice = voice,
  verbose = verbose,
  subtitles = subtitles
)

unlink(paste(input, "files", sep="_"), recursive=TRUE)
unlink(markdown)
