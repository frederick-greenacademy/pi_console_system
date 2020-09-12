import { Component, ElementRef, OnInit, Renderer2, ViewChild, HostListener, OnDestroy, AfterViewInit } from '@angular/core';

@Component({
  selector: 'app-image-register',
  templateUrl: './image-register.component.html',
  styleUrls: ['./image-register.component.css']
})

export class ImageRegisterComponent implements OnInit, OnDestroy {
  @ViewChild('video', { static: true }) videoElement: ElementRef;
  @ViewChild('canvas', { static: true }) canvas: ElementRef;

  isMobileBrowser = true;
  videoWidth = 0;
  videoHeight = 0;
  imgURL: any

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

  constructor(private renderer: Renderer2,
    private el: ElementRef) {

  }

  ngOnInit(): void {
    this.isMobileBrowser = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent)
    if (this.isMobileBrowser == false) {
      this.startCamera()
    }
  }

  handleFileInput(files: FileList) {
    //alert(files.item(0))
    // const context2d = this.canvas.nativeElement.getContext('2d');
    // var imageData = context2d.createImageData(files.item(0), this.canvas.nativeElement.width, this.canvas.nativeElement.height);

    // context2d.putImageData(imageData, 0, 0);

    this.preview(files)

  }

  preview(files: any) {
    if (files.length === 0)
      return;

    var mimeType = files[0].type;
    if (mimeType.match(/image\/*/) == null) {
      // this.message = "Only images are supported.";
      return;
    }

    var reader = new FileReader();
    reader.readAsDataURL(files[0]);
    reader.onload = (_event) => {
      this.imgURL = reader.result;
    }
  }


  @HostListener('window:popstate', ['$event']) onPopState(event: any) {
    console.log('Back button pressed', event);
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

  handleError(error) {
    console.log('Error: ', error);
  }

  attachVideo(stream: any) {
    this.mediaStream = stream;
    console.log('Stream info: ', stream)
    this.renderer.setProperty(this.videoElement.nativeElement, 'srcObject', stream);
    this.renderer.listen(this.videoElement.nativeElement, 'play', (event) => {
      this.videoHeight = this.videoElement.nativeElement.videoHeight;
      this.videoWidth = this.videoElement.nativeElement.videoWidth;
    });
  }

  capture() {
    this.renderer.setProperty(this.canvas.nativeElement, 'width', this.videoWidth);
    this.renderer.setProperty(this.canvas.nativeElement, 'height', this.videoHeight);
    // this.canvas.nativeElement.getContext('2d').drawImage(this.videoElement.nativeElement, 0, 0);
    const context2d = this.canvas.nativeElement.getContext('2d');
    context2d.drawImage(this.videoElement.nativeElement, 0, 0);

    let imageData: ImageData = null;
    imageData = context2d.getImageData(0, 0, this.canvas.nativeElement.width, this.canvas.nativeElement.height);
    console.log('Image data: ', imageData)
  }

  private stopMediaTracks() {

    if (this.mediaStream && this.mediaStream.getTracks) {
      // getTracks() returns all media tracks (video+audio)
      this.mediaStream.getTracks()
        .forEach((track: MediaStreamTrack) => track.stop());
    }
  }

  public ngOnDestroy(): void {
    this.stopMediaTracks();
  }
}
