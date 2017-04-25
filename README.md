Pipeline is:

a) Whole sequence:
config.cfg -> set chunks to None -> execute jpred_queque.exe -> if some
downloads will fail -> execute jpred_fasta.exe -> execute analysis.exe

b) Truncated sequence:
config.cfg -> set chunks to odd number >= 21 -> execute
chunks_generator.exe -> execute jpred_fasta.exe -> if some downloads will
fail -> execute jpred_fasta.exe again -> execute chunks_analysis.exe

Have fun!
