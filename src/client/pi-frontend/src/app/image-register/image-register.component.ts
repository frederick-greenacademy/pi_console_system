import { Component, ElementRef, OnInit, Renderer2, ViewChild, HostListener, OnDestroy } from '@angular/core';

@Component({
  selector: 'app-image-register',
  templateUrl: './image-register.component.html',
  styleUrls: ['./image-register.component.css']
})
export class ImageRegisterComponent implements OnInit, OnDestroy {
  @ViewChild('video', { static: true }) videoElement: ElementRef;
  @ViewChild('canvas', { static: true }) canvas: ElementRef;

  videoWidth = 0;
  videoHeight = 0;

  constraints = {
    // video: {
    //   facingMode: "environment",
    //   width: { ideal: 4096 },
    //   height: { ideal: 2160 }
    // }
    audio: false,
    video: {
      facingMode: "user",
      width: { min: 1024, ideal: 1280, max: 1920 },
      height: { min: 576, ideal: 720, max: 1080 }
    }
  };

  video: any;
  mediaStream: MediaStream = null;

  constructor(private renderer: Renderer2, private el: ElementRef) { }

  ngOnInit(): void {
    this.video = this.videoElement.nativeElement;
    this.startCamera();
  }

  @HostListener('window:popstate', ['$event'])
  onPopState(event) {
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
      alert('Rất tiếc, camera không tìm thấy.');
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
    this.canvas.nativeElement.getContext('2d').drawImage(this.videoElement.nativeElement, 0, 0);
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
