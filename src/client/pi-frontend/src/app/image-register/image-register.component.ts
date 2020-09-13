import { Component, ElementRef, OnInit, Renderer2, ViewChild, HostListener, OnDestroy, AfterViewInit } from '@angular/core';
import { AuthenticationHandler } from '../services/authentication.service';

@Component({
  selector: 'app-image-register',
  templateUrl: './image-register.component.html',
  styleUrls: ['./image-register.component.css']
})

export class ImageRegisterComponent implements OnInit, OnDestroy {
  @ViewChild('video', { static: true }) videoElement: ElementRef;
  @ViewChild('canvas', { static: true }) canvas: ElementRef;
  @ViewChild('canvas2', { static: true }) canvas2: ElementRef;
  @ViewChild('canvas3', { static: true }) canvas3: ElementRef;
  @ViewChild('canvas4', { static: true }) canvas4: ElementRef;
  @ViewChild('canvas5', { static: true }) canvas5: ElementRef;
  @ViewChild('canvas6', { static: true }) canvas6: ElementRef;

  isMobileBrowser = true;
  videoWidth = 0;
  videoHeight = 0;
  imgURL: any
  imageDatas: File[] = []
  nextNumberImage: number = 0


  constraints = {
    audio: false,
    video: {
      facingMode: "environment",
      width: { min: 1024, max: 1920 },
      height: { min: 576, max: 1080 },
      frameRate: { ideal: 10, max: 15 }
    }
  };
  mediaStream: MediaStream = null;

  constructor(
    private renderer: Renderer2,
    private el: ElementRef,
    private serviceHandler: AuthenticationHandler) {

  }

  ngOnInit(): void {
    this.isMobileBrowser = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent)
    if (this.isMobileBrowser == false) {
      this.startCamera()
    }
  }

  handleFileInput(files: FileList) {
    this.preview(files)
  }

  preview(files: any) {
    if (files.length === 0)
      return;

    var mimeType = files[0].type;
    if (mimeType.match(/image\/*/) == null) {
      // chỉ hỗ trợ cho tệp là loại ảnh
      return;
    }

    var reader = new FileReader();
    reader.readAsDataURL(files[0]);
    reader.onload = (_event) => {
      this.imgURL = reader.result;
    }
  }

  @HostListener('window:popstate', ['$event']) onPopState(event: any) {
    console.log('Nhấn quay lại với sự kiện:', event);
  }

  startCamera() {
    this.stopMediaTracks()

    if (!!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)) {
      navigator.mediaDevices.getUserMedia(this.constraints)
        .then(
          this.attachVideo.bind(this))
        .catch(this.handleError);
    } else {
      alert('Rất tiếc, camera chưa sẵn sàng.');
    }
  }

  handleError(error: any) {
    console.log('Có lỗi: ', error);
  }

  attachVideo(stream: any) {
    this.mediaStream = stream;
    console.log('Thông tin một dòng chảy hình ảnh/âm thanh: ', stream)
    this.renderer.setProperty(this.videoElement.nativeElement, 'srcObject', stream);
    this.renderer.listen(this.videoElement.nativeElement, 'play', (event) => {
      this.videoHeight = this.videoElement.nativeElement.videoHeight;
      this.videoWidth = this.videoElement.nativeElement.videoWidth;
    });
  }

  capture() {
    switch (this.nextNumberImage) {
      case 0:
        this.renderer.setProperty(this.canvas.nativeElement, 'width', this.videoWidth);
        this.renderer.setProperty(this.canvas.nativeElement, 'height', this.videoHeight);
        this.canvas.nativeElement.getContext('2d').drawImage(this.videoElement.nativeElement, 0, 0);
        // var imageData: ImageData = this.canvas.nativeElement.getContext('2d').getImageData(0, 0, this.canvas.nativeElement.width, this.canvas.nativeElement.height);
        
        var imageBase64 = this.canvas.nativeElement.toDataURL('image/jpeg')
        if (imageBase64) {
          this.nextNumberImage = 1;
          var xBlob = this.dataURItoBlob(imageBase64)
          var file = new File([xBlob], "file0.jpeg", { type: "'image/jpeg'" })
          this.imageDatas.push(file)
        }

        break
      case 1:
        this.renderer.setProperty(this.canvas2.nativeElement, 'width', this.videoWidth);
        this.renderer.setProperty(this.canvas2.nativeElement, 'height', this.videoHeight);
        this.canvas2.nativeElement.getContext('2d').drawImage(this.videoElement.nativeElement, 0, 0);

        var imageBase64 = this.canvas2.nativeElement.toDataURL('image/jpeg')
        if (imageBase64) {
          this.nextNumberImage = 2;
          var xBlob = this.dataURItoBlob(imageBase64)
          var file = new File([xBlob], "file0.jpeg", { type: "'image/jpeg'" })
          this.imageDatas.push(file)
        }
        break
      case 2:
        this.renderer.setProperty(this.canvas3.nativeElement, 'width', this.videoWidth);
        this.renderer.setProperty(this.canvas3.nativeElement, 'height', this.videoHeight);
        this.canvas3.nativeElement.getContext('2d').drawImage(this.videoElement.nativeElement, 0, 0);

        var imageBase64 = this.canvas3.nativeElement.toDataURL('image/jpeg')
        if (imageBase64) {
          this.nextNumberImage = 3;
          var xBlob = this.dataURItoBlob(imageBase64)
          var file = new File([xBlob], "file0.jpeg", { type: "'image/jpeg'" })
          this.imageDatas.push(file)
        }

        break
      case 3:
        this.renderer.setProperty(this.canvas4.nativeElement, 'width', this.videoWidth);
        this.renderer.setProperty(this.canvas4.nativeElement, 'height', this.videoHeight);
        this.canvas4.nativeElement.getContext('2d').drawImage(this.videoElement.nativeElement, 0, 0);
        var imageBase64 = this.canvas4.nativeElement.toDataURL('image/jpeg')
        if (imageBase64) {
          this.nextNumberImage = 4;
          var xBlob = this.dataURItoBlob(imageBase64)
          var file = new File([xBlob], "file0.jpeg", { type: "'image/jpeg'" })
          this.imageDatas.push(file)
        }
        break
      case 4:
        this.renderer.setProperty(this.canvas5.nativeElement, 'width', this.videoWidth);
        this.renderer.setProperty(this.canvas5.nativeElement, 'height', this.videoHeight);
        this.canvas5.nativeElement.getContext('2d').drawImage(this.videoElement.nativeElement, 0, 0);

        var imageBase64 = this.canvas5.nativeElement.toDataURL('image/jpeg')
        if (imageBase64) {
          this.nextNumberImage = 5;
          var xBlob = this.dataURItoBlob(imageBase64)
          var file = new File([xBlob], "file0.jpeg", { type: "'image/jpeg'" })
          this.imageDatas.push(file)
        }
        break
      case 5:
        this.renderer.setProperty(this.canvas6.nativeElement, 'width', this.videoWidth);
        this.renderer.setProperty(this.canvas6.nativeElement, 'height', this.videoHeight);
        this.canvas6.nativeElement.getContext('2d').drawImage(this.videoElement.nativeElement, 0, 0);

        var imageBase64 = this.canvas6.nativeElement.toDataURL('image/jpeg')
        if (imageBase64) {
          this.nextNumberImage = 1;
          var xBlob = this.dataURItoBlob(imageBase64)
          var file = new File([xBlob], "file0.jpeg", { type: "'image/jpeg'" })
          this.imageDatas.push(file)
        }
        break
    }

  }

  dataURItoBlob(dataURI: any) {

    // chuyển đổi phần dữ liệu base64/URLEncoded đến dữ liệu nhị phân nắm giữ trong chuỗi
    var byteString: any;
    if (dataURI.split(',')[0].indexOf('base64') >= 0)
      byteString = atob(dataURI.split(',')[1]);
    else
      byteString = unescape(dataURI.split(',')[1]);

    // tách ra các phần để lấy đôi của ảnh như là .jpg hay .png
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

    // ghi các bytes của chuỗi đến loại mảng kiểu Uint8Array
    var ia = new Uint8Array(byteString.length);
    for (var i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
    }

    return new Blob([ia], { type: mimeString });
  }

  register() {
    var formData = new FormData()
    let lengthOfImages = this.imageDatas.length
    formData.append('number_image_files', lengthOfImages.toString())

    for (let index = 0; index < lengthOfImages; index++) {
      formData.append('files[]', this.imageDatas[index], 'file' + index + '.jpg')
    }

    this.serviceHandler.uploadFiles(formData)
  }

  setNextNumberImage(e: number) {
    this.nextNumberImage = e
  }
  private stopMediaTracks() {

    if (this.mediaStream && this.mediaStream.getTracks) {
      // lặp lại tìm kiếm các bản ghi để tắt chúng đi
      this.mediaStream.getTracks()
        .forEach((track: MediaStreamTrack) => track.stop());
    }
  }

  public ngOnDestroy(): void {
    this.stopMediaTracks();
  }
}
