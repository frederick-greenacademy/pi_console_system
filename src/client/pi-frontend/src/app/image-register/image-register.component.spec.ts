import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ImageRegisterComponent } from './image-register.component';

describe('ImageRegisterComponent', () => {
  let component: ImageRegisterComponent;
  let fixture: ComponentFixture<ImageRegisterComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ImageRegisterComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ImageRegisterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
