import { Button } from '@material-ui/core';
import Grid from '@material-ui/core/grid';
import resumeTheme from '../theme';
import { useTheme, createStyles, makeStyles } from '@material-ui/core/styles';
import JsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import { useReactToPrint } from 'react-to-print';

const useStyles = makeStyles((theme) =>
    createStyles({
        downloadButton: {
            margin: '20px 0 0 0',
            padding: '0 10px 0 10px',
            float: 'left',
            color: 'primary'
        }


    }),
);

function DownloadPDF({ resumeRef }) {
    const handlePrint = useReactToPrint({
        content: () => resumeRef.current,
    });

    const theme = resumeTheme(useTheme());
    const classes = useStyles(theme);
    const handleDownloadPdf = async () => {
        const element = document.querySelector(".resume");
        const canvas = await html2canvas(element);
        const data = canvas.toDataURL('image/png');
        const pdf = new JsPDF('portrait', 'pt', 'a4');
        const imgProperties = pdf.getImageProperties(data);
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight =
            (imgProperties.height * pdfWidth) / (imgProperties.width);

        pdf.addImage(data, 'PNG', 40, 40, pdfWidth - 80, pdfHeight - 40);
        pdf.save('print.pdf');
    };


    return (
        <Grid item container spacing={1}>
            <Grid item>
                <Button onClick={handleDownloadPdf} variant='contained' color='primary' className={classes.downloadButton}>Download PDF</Button>
            </Grid>
            <Grid item>
                <Button onClick={handlePrint} variant='contained' className={classes.downloadButton}>Export to pdf</Button>
            </Grid>

        </Grid>

    );
}

export default DownloadPDF;
