Nama : Maurilla Maharani Nur Abdul

NPM : 2506588374

Kelas : PBP C

### Tugas 2
1. Ketika user membukan halaman portofolio, browser akan mengirimkan request ke server Django. Request tersebut akan diproses melalui URL configuration oleh project urls.py. Lalu app urls.py akan menentukan view yang dipanggil. Pada file tersebut, URL /experience/ diarahkan ke fungsi show_experience yang akan mengambil data experience dari model Experience yang kemudian dimasukkan ke dalam dictionary context. Model experience mendefinisikan struktur data, seperti title, description, category dll. Ini digunakan untuk mengambil data dari database tanpa harus menulis SQL secara langsung. View mengirimkan context ke template experience.html untuk memberntuk tampilan halaman experience. Setelah semua itu, browser menampilkan halaman experience yang berisi data experience. 

2. Data disimpan pada model karena model bertanggung jawab untuk mengelola data, sedangkan template bertanggung jawab untuk menampilkan data. Pada project saya, data experience disimpan pada model Experience yang memiliki beberapa field seperti title, description, category dll. Menyimpan data pada model membuat data lebih mudah diperbarui, memisahkan tanggung jawab antar file, dan menghindari duplikasi data karena model bertanggung jawab sepenuhnya pada penyimpanan data.

3. Perintah makemigrations digunakan untuk membuat file migration berdasarkan perubahan yang dilakukan pada model. File ini berisi instruksi mengenai perubahan struktur database yang perlu dilakukan. Sedangkan perintah migrate digunakan untuk menerapkan migration yang telah dibuat ke database. Contoh penggunaan adalah ketika mengubah models.py dengan menambahkan/mengurangi field atau class. Ketika melakukan perubahan tersebut, maka diharuskan menjalankan perintah makemigrations dan migrate agar database terupdate strukturnya sesuai yang diinginkan.

Saya tidak menggunakan AI dalam proses pembuatan tutorial 2 maupun tugas 2.

