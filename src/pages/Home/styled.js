import styled from 'styled-components';

const AppContainer = styled.div`
  display: flex;
	gap: 40px;
	flex-direction: column;
	padding: 40px 20px;
`;

const Button = styled.button`
	width: 320px;
	height: 70px;
	background: #136BDE;
	border-radius: 8px;
	border: none;

	font-weight: 400;
	font-size: 36px;
	line-height: 42px;
	color: #FFFEFE;
	cursor: pointer;
`;

const ImagesContainer = styled.div`
	display: flex;
	flex-direction: row;
	align-items: center;
	img {
		flex: 1;
	}
	${Button} {
		background: #23D84D;
	}
	gap: 40px;
`;

const CameraButtonContainer = styled.div`
	display: flex;
	flex-direction: row;
	${Button}:nth-child(2) {
		margin-left: 250px;
		width: 200px;
		background: #E7041A;
	}
`;

const Styled = { AppContainer, Button, ImagesContainer, CameraButtonContainer }

export default Styled;
