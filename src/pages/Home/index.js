import { useState, useRef } from 'react';
import Styled from './styled';

export function HomePage() {
  const [image, setImage] = useState(null);
  const inputImage = useRef(null);

  const handleOnUploadImage = event => {
    if (event.target.files && event.target.files[0]) {
      let img = event.target.files[0];
      setImage(URL.createObjectURL(img));
    }
  }

  const handleOnClickUploadButton = event => {
    inputImage.current.click();
  }

  return (
    <Styled.AppContainer>
      <Styled.ImagesContainer>
        <div style={{ flexBasis: "40%" }}>
          <img src={image} alt="image" />
        </div>
        <Styled.Button>Start Detect</Styled.Button>
        <div style={{ flexBasis: "40%" }}>
          <img src="https://www.w3schools.com/css/img_chania.jpg" alt="image" />
        </div>
      </Styled.ImagesContainer>
      <input style={{ display: 'none' }} ref={inputImage} type="file" onChange={handleOnUploadImage} placeholder="Load Image" />
      <Styled.Button onClick={handleOnClickUploadButton}>Load Image</Styled.Button>
      <div>
        <div>Camera IP</div>
        <div style={{ width: 320, fontSize: 30, height: 60, border: '1px solid black', borderRadius: 8, textAlign: 'center', lineHeight: '60px' }}>
          01.01.01.01
        </div>
      </div>
      <Styled.CameraButtonContainer>
        <Styled.Button>Connect Camera</Styled.Button>
        <Styled.Button>Stop</Styled.Button>
      </Styled.CameraButtonContainer>
    </Styled.AppContainer>
  );
}
