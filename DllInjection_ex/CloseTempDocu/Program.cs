using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Excel =  Microsoft.Office.Interop.Excel;
using Word = Microsoft.Office.Interop.Word;
using PowerPoint = Microsoft.Office.Interop.PowerPoint;
using System.Runtime;
using System.Windows.Forms;

namespace CloseTempDocu
{

   
    class Program
    {
        static void CloseWord(string filePath)
        {
            bool flag_exist = true;
            

            while (flag_exist)
            {
                try
                {
                    Word.Application app = (Word.Application)System.Runtime.InteropServices.Marshal.GetActiveObject("Word.Application");
                    if (app == null)
                    {
                        continue;
                    }

                    foreach (Word.Document docu in app.Documents)
                    {
                        if (docu.FullName == filePath)
                        {
                            object saveOption = Word.WdSaveOptions.wdDoNotSaveChanges;
                            object originalFormat = Word.WdOriginalFormat.wdOriginalDocumentFormat;
                            object routeDocument = false;

                            docu.Close(ref saveOption, ref originalFormat, ref routeDocument);

                            flag_exist = false;
                        }

                    }
                }
                catch(System.Runtime.InteropServices.COMException)
                {
                    continue;
                }
                
            }
            

            
            
        }

        static void CloseExcel(string filePath)
        {
            bool flag_exist = true;
            while (flag_exist)
            {
                try
                {
                    Excel.Application app = (Excel.Application)System.Runtime.InteropServices.Marshal.GetActiveObject("Excel.Application");
                    if (app == null)
                    {
                        continue;

                    }

                    foreach (Excel.Workbook workbook in app.Workbooks)
                    {
                        if (workbook.FullName == filePath)
                        {
                            object saveOption = Excel.XlSaveAction.xlDoNotSaveChanges;

                            workbook.Close(saveOption, false, false);
                            flag_exist = false;
                        }
                    }
                }
                catch (System.Runtime.InteropServices.COMException)
                {
                    continue;
                }
                
            }
            
        }

        static void ClosePPT(string filePath)
        {
            bool flag_exists = true;
            while (flag_exists)
            {
                try { 
                    PowerPoint.Application app = (PowerPoint.Application)System.Runtime.InteropServices.Marshal.GetActiveObject("PowerPoint.Application");
                    if(app == null)
                    {
                        continue;
                    }

                    foreach (PowerPoint.Presentation present in app.Presentations)
                    {
                        if (present.FullName == filePath)
                        {
                            present.Close();
                            flag_exists = false;
                        }
                    }
                }
                catch (System.Runtime.InteropServices.COMException)
                {
                    continue;
                }
            }
            
        }
        static void Main(string[] args)
        {

            string filename = args[0];
            Console.WriteLine(filename);


            filename = filename.Replace("\"", "");
            filename = filename.Replace("\\\\", "\\");
            filename = filename.Replace("\'", "");
           
            Console.WriteLine(filename);
            string[] ext = filename.Split('.');
            string filterExt = ext[ext.Length - 1];

            if (filterExt.Contains("doc"))
            {
                CloseWord(filename);
            }
            else if(filterExt.Contains("ppt"))
            {
                ClosePPT(filename);
            }
            else if(filterExt.Contains("xls"))
            {
                CloseExcel(filename);
            }

        }
    }
}
