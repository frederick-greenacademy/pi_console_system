import { Component, ElementRef, OnInit, Renderer2, ViewChild, HostListener } from '@angular/core';
var localStream;
@Component({
  selector: 'app-image-register',
  templateUrl: './image-register.component.html',
  styleUrls: ['./image-register.component.css']
})
export class ImageRegisterComponent implements OnInit {
  @ViewChild('video', { static: true }) videoElement: ElementRef;
  @ViewChild('canvas', { static: true }) canvas: ElementRef;

  videoWidth = 0;
  videoHeight = 0;

  constraints = {
    video: {
      facingMode: "environment",
      width: { ideal: 4096 },
      height: { ideal: 2160 }
    }
  };

  constructor(private renderer: Renderer2, private el: ElementRef) { }

  ngOnInit(): void {
    this.startCamera();
  }
  MediaStream: any;
  @HostListener('window:popstate', ['$event'])
  onPopState(event) {
    console.log('Back button pressed', event);
    // this.renderer.destroy()
    // localStream.getVideoTracks()[0].stop();
    // localStream = null;
    const tracks = localStream.getTracks();

    // Tracks are returned as an array, so if you know you only have one, you can stop it with: 
    tracks[0].stop();

    // Or stop all like so:
    tracks.forEach(track => track.stop())
    // this.renderer.setProperty
    // this.renderer.removeChild(this.el.nativeElement, this.videoElement.nativeElement);

  }

  startCamera() {
    if (!!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)) {
      navigator.mediaDevices.getUserMedia(this.constraints).then(this.attachVideo.bind(this)).catch(this.handleError);
    } else {
      alert('Sorry, camera not available.');
    }
  }

  handleError(error) {
    console.log('Error: ', error);
  }

  attachVideo(stream) {
    // this.renderer.setProperty(this.videoElement.nativeElement, 'srcObject', stream);
    this.renderer.setProperty(this.videoElement.nativeElement, 'srcObject', stream);
    this.renderer.listen(this.videoElement.nativeElement, 'play', (event) => {
      this.videoHeight = this.videoElement.nativeElement.videoHeight;
      this.videoWidth = this.videoElement.nativeElement.videoWidth;
    });
    localStream = stream; // create the stream tracker
  }

  capture() {
    this.renderer.setProperty(this.canvas.nativeElement, 'width', this.videoWidth);
    this.renderer.setProperty(this.canvas.nativeElement, 'height', this.videoHeight);
    this.canvas.nativeElement.getContext('2d').drawImage(this.videoElement.nativeElement, 0, 0);
  }
}
